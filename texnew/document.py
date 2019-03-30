import re
import itertools

from .file import read_file
from . import __version__

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def _strip_block(clist):
    """Removes trailing whitespace from an input list for a block"""
    end = -1
    for i,e in reversed(list(enumerate(clist))):
        if e:
            end = i
            break
    start = 0
    for i,e in enumerate(clist):
        if e:
            start = i
            break
    return clist[start:end+1]

class Divider:
    """Divider class primarily to be used in the document class"""
    def __init__(self, start_symb, fill, length=80):
        if len(fill) != 1:
            raise ValueError("fill must be a string of length 1")
        self.fill = fill
        self.start = start_symb
        self.length = length
    def gen(self, name):
        if len(name) >= self.length:
            raise ValueError("divider name is too long")
        return (self.start + " " + name + " ").ljust(self.length, self.fill)
    def is_div(self, test):
        test = test.rstrip()
        return test.startswith(self.start) and test.endswith(self.fill) and len(test) == self.length
    def name(self, div):
        pat = re.compile("{} (.*) {}*".format(self.start, self.fill))
        res = pat.search(div)
        if res:
            return res.group(1)
        else:
            return None

class Document:
    """A custom method that emulates the python 'dict', but with different construction methods and an inherent order in the keys.
    Also has string methods to appear as a proper block-based document

    sub_list: a dict of possible substitutions to make
    defaults: a dict of fallback values when passed a 'Falsey' value for a block
    div_func: the divider used when printing the Document
    buf: number of newlines to place at end of printing block
    """
    def __init__(self, sub_list={}, defaults={}, div_func=None,buf=0):
        self.div = div_func
        self.subs = sub_list
        self._blocks = {}
        self._order = [] # order matters here!
        self.buf=buf
        self.defaults = defaults

    # return a representation of this object (_blocks and blocks)
    def __repr__(self):
        return "Blocks:\n"+repr(self._blocks) + "\nOrder:\n" + repr(self._order)

    # return a string of this object (e.g. for printing)
    def __str__(self):
        output = ""
        for block in self._order:
            if self.div:
                output += self.div.gen(block) + "\n"
            output += "\n".join(self._blocks[block]) + "\n"*(self.buf+1)
        return output 

    # write to a document
    # TODO: error handling here, perhaps in some more generic write method
    def write(self,fname):
        with open(fname,'a+') as f:
            f.write(str(self))

    # access document indices as blocks
    def __getitem__(self,bname):
        return self._blocks[bname]

    # emulate python dict.get
    def get(self, bname, rep=[]):
        if bname in self._order:
            return self._blocks[bname]
        else:
            return rep

    # check has block
    def __contains__(self,bname):
        return bname in self._blocks

    # add _blocks, will replace if it already exists
    def __setitem__(self, bname, content_list):
        # can input blank content_list in any 'False' format
        if not content_list:
            content_list = self.defaults.get(bname,[])

        # remove trailing whitespace, starting and ending blank lines
        content_list = _strip_block([l.rstrip() for l in content_list])
        
        # substitute matches in content_list with sub_list
        repl_match = lambda x: r"<\+" + str(x) + r"\+>"
        for k in self.subs.keys():
            content_list = [re.sub(repl_match(k), str(self.subs[k]), l) for l in content_list]

        # add _blocks, blocks; overwrites
        self._blocks[bname] = content_list
        if bname not in self._order:
            self._order += [bname]
    
    # returns empty block if not contained
    def __missing__(self,bname):
        return []

    # delete block
    def __delitem__(self, bname):
        del self._blocks[bname]
        self._order.remove(bname)

class TexnewDocument(Document):
    """A special class of type Document with custom loading and checking types, along with a LaTeX style block delimiter"""
    def __init__(self, sub_list={},defaults={}):
        # create default settings when inputting block (if block is none)
        new_defs = {
            'header': ["% Template created by texnew (author: Alex Rutar); info can be found at 'https://github.com/alexrutar/texnew'.",
                    "% version ({})".format(__version__)
                ],
            'file-specific preamble': ["% REPLACE"],
            'document start': ["REPLACE", "\\end{document}"]
        }
        super().__init__(sub_list, div_func=Divider("%","-"), defaults={**new_defs,**defaults}, buf=2)

    # loads a file and appends blocks to current block list
    def load(self,target):
        fl = read_file(target,src="user")
        # read the dividers
        divs = [(i,self.div.name(l)) for i,l in enumerate(fl) if self.div.is_div(l)]

        # break at dividers
        for f,g in _pairwise(divs):
            self[f[1]] =  fl[f[0]+1:g[0]-1]
        self[divs[-1][1]] = fl[divs[-1][0]+1:]
    # TODO: will eventually create an error verification script which consumes a LaTeXDocumet to check that it is an (error-free) LaTeX document
    # TODO: write comparison methods ?
