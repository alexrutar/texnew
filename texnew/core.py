import re

from . import __version__
from .file_mgr import get_div, read_file
from .error import TexnewFileError

# load template information
def load_template(template_type):
    try:
        return read_file("templates",template_type,method="yaml")
    except TexnewFileError as e:
        e.context = "template"
        e.context_info['type'] = template_type
        raise e

# load user information
def load_user(info_name = "default"):
    try:
        return read_file("user",info_name,method="yaml")
    except TexnewFileError as e:
        e.context = "user"
        e.context_info['name'] = info_name
        raise e

# a generic datatype representing a LaTeX document, composed of blocks
# may not actually be a proper LaTeX document (that's up to you to decide)
# TODO: will eventually create an error verification script which consumes a LaTeXDocumet to check that it is an (error-free) LaTeX document
# TODO: write comparison methods ?
class LaTeXDocument:
    # when creating sub_list, make sure to add template **after** to not be overwritten by user file
    def __init__(self, sub_list={}, div_func=get_div):
        self.div = div_func
        self.subs = sub_list
        self.components = {}
        self.blocks = [] # order matters here!

    # add components
    def set_component(self, comp_name, contents):
        # substitute matches in contents with sub_list
        repl_match = lambda x: r"<\+" + str(x) + r"\+>"
        for k in self.subs.keys():
            contents = re.sub(repl_match(k), str(self.subs[k]), contents)
        self.components[comp_name] = contents
        self.blocks += [comp_name]

    # generate the actual file (as a string)
    def gen_file(self):
        output = ""
        for comp in self.blocks:
            output += self.div(comp)
            output += self.components[comp]
            output += "\n"
        return output 

# builds a custom LaTeXDocument from a template data dictionary
# makes a lot of assumptions about the structure of the dictionary, or will break!
def run(template_data, sub_list={}, user_macros={}):
    # merge sub_list
    sub_list["doctype"] = template_data["doctype"]
    doc = LaTeXDocument(sub_list)

    # relative internal path
    rel = ["share", template_data["template"]]

    # header
    header = "% Template created by texnew (author: Alex Rutar); info can be found at 'https://github.com/alexrutar/texnew'.\n"
    header += "% version ({})\n".format(__version__)
    doc.set_component("header", header)

    # default components
    doc.set_component("doctype", read_file(*rel,"defaults","doctype.tex"))
    doc.set_component("packages", read_file(*rel,"defaults","packages.tex"))
    doc.set_component("default macros", read_file(*rel,"defaults","macros.tex"))

    # special macros
    for name in template_data['macros']:
        doc.set_component("macros ({})".format(name), read_file(*rel,"macros",name + ".tex",method="str"))
    
    # add space for user macros, or placeholder
    # TODO: change user_macros to be a string
    if 'macros' in user_macros.keys():
        fstring = "".join(user_macros['macros'])
    else:
        fstring = "% REPLACE\n"
    doc.set_component("file-specific preamble", fstring)

    # formatting component
    doc.set_component("formatting", read_file(*rel,"formatting",template_data['formatting']+ ".tex"))

    # check for contents in user_macros to fill document
    # TODO: change contents to be a string
    if 'contents' in user_macros.keys():
        fstring = "".join(user_macros['contents'])
    else:
        fstring = "\nREPLACE\n" + "\\end{document}\n"
    doc.set_component("document start", fstring)

    return doc

