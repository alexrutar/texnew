import yaml
import os
import re

from . import __version__
from .file_mgr import rpath, get_div, read_file
from .error import TexnewInputError, TexnewFileError

# print a divider to the specified output
def write_div(out, name):
    out.write("\n" + get_div(name))

# creates a matching regex for file substitution
def repl_match(name):
    if name == "any":
        return r"<\+.*\+>"
    else:
        return r"<\+" + str(name) + r"\+>"

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

# somehow remove template generation? is it worth it
# the main file-building function
# data = load_template(template_type)
# user_info = load_user(aname)
# merge error types
def run(target,data,user_info,user_macros={}):
    tex_doctype = re.sub(repl_match("doctype"), data['doctype'], read_file("share","defaults","doctype.tex",method="str"))
    tex_packages = read_file("share","defaults","packages.tex",method="str")
    tex_macros = read_file("share","defaults","macros.tex",method="str")
    tex_formatting = read_file("share","formatting",data['formatting'] + '.tex',method="str")
    
    # substitute user_info
    for k in user_info.keys():
        tex_formatting = re.sub(repl_match(k), str(user_info[k]), tex_formatting)

    # generate output file
    with open(target,"a+") as output:
        output.write("% Template created by texnew (author: Alex Rutar); info can be found at 'https://github.com/alexrutar/texnew'.\n")
        output.write("% version ({})\n".format(__version__))

        # create doctype
        write_div(output, "doctype")
        output.write(tex_doctype)

        # add default packates
        write_div(output, "packages")
        output.write(tex_packages)

        # add included macros
        write_div(output, "default macros")
        output.write(tex_macros)
        for name in data['macros']:
            write_div(output, name+" macros")
            output.write(read_file("share","macros",name + ".tex",method="str"))

        # add space for user macros
        write_div(output, "file-specific macros")
        if 'macros' in user_macros.keys():
            for l in user_macros['macros']:
                output.write(l)
        else:
            output.write("% REPLACE\n")

        # add formatting file
        write_div(output, "formatting")
        output.write(tex_formatting)

        # check for contents in user_macros to fill document
        write_div(output, "document start")
        if 'contents' in user_macros.keys():
            for l in user_macros['contents']:
                output.write(l)
        else:
            output.write("\nREPLACE\n")
            output.write("\\end{document}\n")

