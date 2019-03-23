import yaml
import os
import re

from . import __version__
from .file_mgr import filestring, truncated_files, rpath, get_div

# print a divider to the specified output
def write_div(out, name):
    out.write("\n" + get_div(name))

# creates a matching regex for file substitution
def repl_match(name):
    if name == "any":
        return r"<\+.*\+>"
    else:
        return r"<\+" + str(name) + r"\+>"

# the main file-building function
def run_output(target,template_type,data,user_info,user_macros):
    tex_doctype = re.sub(repl_match("doctype"), data['doctype'], filestring("share","defaults","doctype.tex"))
    tex_packages = filestring("share","defaults","packages.tex")
    tex_macros = filestring("share","defaults","macros.tex")
    tex_formatting = filestring("share","formatting",data['formatting'] + '.tex')
    
    # substitute user_info
    for k in user_info.keys():
        tex_formatting = re.sub(repl_match(k), str(user_info[k]), tex_formatting)

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
            output.write(filestring("share","macros",name + ".tex"))

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

# return yaml information from a relative path
def load_yaml(*rel_path):
    with open(rpath(*rel_path),'r') as source:
        return yaml.load(source)

# load template information
def get_data(template_type):
    data = []
    try:
        data = load_yaml("share","templates",template_type + ".yaml")
    except FileNotFoundError:
        print("The template \"{}\" does not exist! The possible template names are:\n".format(template_type)+ "\t".join(truncated_files("share","templates")))
    return data

# essentially a wrapper for run_output
def run(target, template_type, user_macros={}):
    if os.path.exists(target):
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(target))
    else:
        try:
            user_info = load_yaml("user_private.yaml")
        except FileNotFoundError:
            try:
                user_info = load_yaml("user.yaml")
            except FileNotFoundError:
                user_info = {}
                print("Warning: user info file could not be found at 'user.yaml' or at 'user_private.yaml'.")
        data = get_data(template_type)
        if data:
            run_output(target,template_type,data,user_info,user_macros)
