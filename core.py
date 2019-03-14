import yaml
import os
import re
from file_mgr import filestring, truncated_files, rpath

def write_div(out, name):
    out.write(("\n% " + name + " ").ljust(80, "-") + "\n")

def repl_match(name):
    if name == "any":
        return r"<\+.*\+>"
    else:
        return r"<\+" + str(name) + r"\+>"


def run_output(target,template_type,data,user_info,user_macros):
    tex_doctype = re.sub(repl_match("doctype"), data['doctype'], filestring("src","defaults","doctype.tex"))
    tex_packages = filestring("src","defaults","packages.tex")
    tex_macros = filestring("src","defaults","macros.tex")
    tex_formatting = filestring("src","formatting",data['formatting'] + '.tex')
    for k in user_info.keys():
        tex_formatting = re.sub(repl_match(k), str(user_info[k]), tex_formatting)

    with open(target,"a+") as output:
        # create doctype
        output.write("% Template created by texnew (author: Alex Rutar); info can be found at 'https://github.com/alexrutar/texnew'.")
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
            output.write(filestring("src","macros",name + ".tex"))


        # add space for user macros
        write_div(output, "file-specific macros")
        if user_macros:
            for l in user_macros:
                output.write(l)
        else:
            output.write("% REPLACE\n")

        # add formatting file
        write_div(output, "formatting")
        output.write(tex_formatting)

def load_yaml(*rel_path):
    with open(rpath(*rel_path),'r') as source:
        return yaml.load(source)

def get_data(template_type):
    data = []
    try:
        data = load_yaml("templates",template_type + ".yaml")
    except FileNotFoundError:
        print("The template \"{}\" does not exist! The possible template names are:\n".format(template_type)+ "\t".join(truncated_files("templates")))
    return data

# essentially a wrapper for run_output
def texnew_run(target, template_type, user_macros):
    if os.path.exists(target) and not update:
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(target))
    else:
        try:
            user_info = load_yaml("src","user_private.yaml")
        except FileNotFoundError:
            try:
                user_info = load_yaml("src","user.yaml")
            except FileNotFoundError:
                user_info = {}
                print("Warning: user info file could not be found at 'src/user.yaml' or at 'src/user_private.yaml'. Run 'texnew -i' for more info.")
        data = get_data(template_type)
        if data:
            run_output(target,template_type,data,user_info,user_macros)
