import re
import itertools
import subprocess

# TODO: clean .workspace instead of clean_dir
from .rpath import clean_workspace, RPath
from . import __version__
from pathlib import Path

class Divider:
    """Divider class primarily to be used in the document class"""
    def __init__(self, start_symb, fill, length=80):
        if len(fill) != 1:
            raise ValueError("'fill' must be a string of length 1")
        self.fill = fill
        self.start = start_symb
        self.length = length

    def gen(self, name):
        if len(name) >= self.length-len(self.start)-3:
            raise ValueError("Divider name is too long")
        return (self.start + " " + name + " ").ljust(self.length, self.fill)

    def match(self, search_str):
        """Split an input string on headers, while keeping the header name."""
        pat = "^(?=.{{{:d}}}$){} (.*) {}+$".format(self.length, self.start, self.fill)
        return re.split(pat,search_str,flags=re.M)[1:]


# TODO: perhaps subclass collections.abc.MutableMapping - however, this may not preserve order
# TODO: or, keep dict structure but remove the _order - dict has guaranteed order as of python 3.7
class Document:
    """A custom method that emulates the python 'dict', but with different construction methods and an inherent order in the keys.
    Also has string methods to appear as a proper block-based document

    sub_list: a dict of possible substitutions to make
    defaults: a dict of fallback values when passed a 'Falsey' value for a block
    div_func: the divider used when printing the Document
    buf: number of newlines to place at end of printing block
    """
    def __init__(self, contents, sub_list={}, defaults={}, div_func=None, buf=0):
        self.div = div_func
        self.subs = sub_list
        self._blocks = contents
        self._order = [] # order matters here!
        self.buf=buf
        self.defaults = defaults

    def __repr__(self):
        return "Blocks:\n"+repr(self._blocks) + "\nOrder:\n" + repr(self._order)

    def __str__(self):
        output = ""
        for block in self._order:
            if self.div:
                output += self.div.gen(block) + "\n"
            output += self._blocks[block] + "\n"*(self.buf+1)
        return output 

    def write(self,path):
        """Write to a document"""
        path.write_text(str(self))

    def __getitem__(self,bname):
        return self._blocks[bname]

    def get(self, bname, rep=""):
        if bname in self._order:
            return self._blocks[bname]
        else:
            return rep

    def __contains__(self,bname):
        return bname in self._blocks

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
    
    def __missing__(self,bname):
        return ""

    def __delitem__(self, bname):
        del self._blocks[bname]
        self._order.remove(bname)


# parse the file for errors
# TODO: this is garbage, fix it (that's probably a lot of work unfortunately)
# TODO: does not catch warnings
def parse_errors(path):
    """Parse the file path for errors."""
    dct = {'errors':[],'warnings':[],'fatal':[]}
    fl = path.read_text().split("\n")

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
    def __init__(self, contents, sub_list={},defaults={}):
        # create default settings when inputting block (if block is none)
        new_defs = {
            'header':("% Template created by texnew (author: Alex Rutar); info can be found at 'https://github.com/alexrutar/texnew'.\n"
                      "% version ({})".format(__version__)),
            'file-specific preamble': "% REPLACE",
            'document start': "REPLACE\n\\end{document}"
        }
        super().__init__(contents, sub_list, div_func=Divider("%","-"), defaults={**new_defs,**defaults}, buf=2)

    # loads a file and appends blocks to current block list
    # TODO: Path, keep this as list, implement read_file with string from path object;
    # just wrap the string object with splitting to get a list, and a yaml read to get a yaml
    @classmethod
    def load(cls,fpath):
        """Constructor for TexnewDocument from filepath"""
        fl = fpath.read_text()

        # check version
        res = re.compile(r"% version \((.*)\)").search(fl)
        if not res or res.group(1).startswith("0"):
            raise FutureWarning("File version is too old!")

        # set blocks
        blocks = Divider("%","-").match(fl)
        dct = {blocks[i]:blocks[i+1] for i in range(0,len(blocks),2)}
        return cls(dct)

    def verify(self):
        """Compile and parse log file for errors."""
        self.write(RPath.workspace() / 'test.tex')

        # compile the template
        lmk_args = [
                'latexmk',
                '-pdf',
                '-interaction=nonstopmode',
                '-outdir={}'.format(RPath.workspace()),
                RPath.workspace() / 'test.tex']
        try:
            subprocess.check_output(lmk_args, stderr=subprocess.STDOUT)

            self.logfile = RPath.workspace() / 'test.log'
            self.errors = parse_errors(RPath.workspace() / 'test.log')
        except subprocess.CalledProcessError as e:
            self.errors = {'latexmk': e.output.decode()}
        clean_workspace()
        return self.errors
