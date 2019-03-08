# Hello

# File Names: doctype, formatting, macros, packages
# main source: main.tex
import yaml
import os
import re

def filestring(rel_path):
    return open(os.path.join(os.path.dirname(__file__),rel_path)).read()

def write_div(out, name):
    out.write(("\n% " + name + " ").ljust(80, "-") + "\n")

def repl_match(name):
    if name == "any":
        return r"<\+.*\+>"
    else:
        return r"<\+" + name + r"\+>"


if __name__ == "__main__":
    with open("test.yaml", 'r') as source:
        data = yaml.load(source)

    tex_doctype = filestring("src/defaults/doctype.tex")
    tex_packages = filestring("src/defaults/packages.tex")
    tex_macros = filestring("src/defaults/macros.tex")
    tex_formatting = filestring("src/formatting/" + data['formatting'] + '.tex')
    tex_main = filestring("src/defaults/main.tex")

    div = "% " + "-"*20


    with open("out.tex","w+") as output:
        # create doctype
        write_div(output, "doctype")
        output.write(re.sub(repl_match("doctype"), data['doctype'], tex_doctype))

        # add default packates
        write_div(output, "packages")
        output.write(tex_packages)

        # add included macros
        write_div(output, "default macros")
        output.write(tex_macros)
        for name in data['macros']:
            write_div(output, name+" macros")
            output.write(filestring("src/macros/" + name + ".tex"))

        # add formatting file
        write_div(output, "formatting")
        output.write(tex_formatting)

        # add main file
        output.write(tex_main)
