import re
import itertools
import subprocess

# TODO: clean .workspace instead of clean_dir
from .file import read_file, clean_workspace
from . import __version__

# TODO: avoid these imports
from .file import rpath

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
    def match(self, search_str):
        """Split an input string on headers, while keeping the header name."""
        pat = "^{} (.*) {}*$".format(self.start, self.fill)
        return re.split(pat,search_str,flags=re.M)
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
        self._blocks = {} # every entry is now a string
        self._order = [] # order matters here!
        self.buf=buf
        self.defaults = defaults

    # return a representation of this object (blocks and order)
    def __repr__(self):
        return "Blocks:\n"+repr(self._blocks) + "\nOrder:\n" + repr(self._order)

    # return a string of this object (e.g. for printing)
    def __str__(self):
        output = ""
        for block in self._order:
            if self.div:
                output += self.div.gen(block) + "\n"
            output += self._blocks[block] + "\n"*(self.buf+1)
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
    def get(self, bname, rep=""):
        if bname in self._order:
            return self._blocks[bname]
        else:
            return rep

    # check has block
    def __contains__(self,bname):
        return bname in self._blocks

    # add _blocks, will replace if it already exists
    def __setitem__(self, bname, cstr):
        # can input blank cstr in any 'False' format
        if not cstr:
            cstr = self.defaults.get(bname,"")

        # remove trailing whitespace, starting and ending blank lines
        cstr = cstr.strip()
        
        # substitute matches in cstr with sub_list
        repl_match = lambda x: r"<\+" + str(x) + r"\+>"
        for k in self.subs.keys():
            cstr = re.sub(repl_match(k), str(self.subs[k]), cstr)

        # add _blocks, blocks; overwrites
        self._blocks[bname] = cstr
        if bname not in self._order:
            self._order.append(bname)
    
    # returns empty block if not contained
    def __missing__(self,bname):
        return ""

    # delete block
    def __delitem__(self, bname):
        del self._blocks[bname]
        self._order.remove(bname)

# parse the file for errors
# TODO: this is garbage, fix it (that's probably a lot of work unfortunately)
# TODO: does not catch warnings
def parse_errors(*rel_path):
    dct = {'errors':[],'warnings':[],'fatal':[]}
    fl = read_file(*rel_path)

    append = False
    temp = ""
    for l in fl:
        if l.startswith("! "):
            dct['fatal'] += [l]
        if l.startswith("./.workspace/test.tex:"):
            temp = l
            append = True
        if append:
            temp += l
        if l.startswith("l."):
            temp += l
            append = False
            dct['errors'] += [temp]
    for key in ['errors','warnings','fatal']:
        if dct[key]:
            return dct
    return {}

class TexnewDocument(Document):
    """A special class of type Document with custom loading and checking types, along with a LaTeX style block delimiter"""
    def __init__(self, sub_list={},defaults={}):
        # create default settings when inputting block (if block is none)
        new_defs = {
            'header':("% Template created by texnew (author: Alex Rutar); info can be found at 'https://github.com/alexrutar/texnew'.\n"
                      "% version ({})".format(__version__)),
            'file-specific preamble': "% REPLACE",
            'document start': "REPLACE\n\\end{document}"
        }
        super().__init__(sub_list, div_func=Divider("%","-"), defaults={**new_defs,**defaults}, buf=2)

    # loads a file and appends blocks to current block list
    # TODO: Path, keep this as list, implement read_file with string from path object;
    # just wrap the string object with splitting to get a list, and a yaml read to get a yaml
    def load(self,target):
        fl = read_file(target,src="user")
        # read the dividers
        divs = [(i,self.div.name(l)) for i,l in enumerate(fl) if self.div.is_div(l)]

        # break at dividers
        for f,g in _pairwise(divs):
            self[f[1]] =  fl[f[0]+1:g[0]-1]
        self[divs[-1][1]] = fl[divs[-1][0]+1:]

    def verify(self):
        """Compile and parse log file for errors."""
        self.write(rpath(".workspace","test.tex"))

        # compile the template
        lmk_args = [
                'latexmk',
                '-pdf',
                '-interaction=nonstopmode',
                '-outdir={}'.format(rpath(".workspace")),
                rpath(".workspace","test.tex")]
        try:
            subprocess.check_output(lmk_args, stderr=subprocess.STDOUT)

            self.logfile = read_file(".workspace","test.log")
            self.errors = parse_errors(".workspace","test.log") # TODO: should return empty dict if there are no errors
        except subprocess.CalledProcessError as e:
            self.errors = {'latexmk': e.output.decode()}
        clean_workspace()
        return self.errors
