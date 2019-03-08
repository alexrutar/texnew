import yaml
import os
import re
import sys
import argparse

def filestring(rel_path):
    return open(os.path.join(os.path.dirname(__file__),rel_path)).read()


def write_div(out, name):
    out.write(("\n% " + name + " ").ljust(80, "-") + "\n")


def repl_match(name):
    if name == "any":
        return r"<\+.*\+>"
    else:
        return r"<\+" + name + r"\+>"


def template_list():
    return [s[:-5] for s in os.listdir(os.path.join(os.path.dirname(__file__),"templates"))]


def parse():
    parser = argparse.ArgumentParser(description='An automatic LaTeX template creator.')
    parser.add_argument('target', metavar='output', type=str, nargs=1,
                                help='the name of the file you want to create')
    parser.add_argument('template_type', metavar='template', type=str, nargs=1,
                                help='the name of the template to use')

    parser.add_argument('-l', "--list", action="store_true", default=False, dest="lst",help="list existing templates")

    args = parser.parse_args()
    target = args.target[0]
    if not target.endswith(".tex"):
        target = target + ".tex"
    template_type = args.template_type[0]
    template_list()

    return (target, template_type)


def run_output(target,template_type,data):
    tex_doctype = filestring("src/defaults/doctype.tex")
    tex_packages = filestring("src/defaults/packages.tex")
    tex_macros = filestring("src/defaults/macros.tex")
    tex_formatting = filestring("src/formatting/" + data['formatting'] + '.tex')

    with open(target,"a+") as output:
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

if __name__ == "__main__":
    if "-l" in sys.argv or "--list" in sys.argv:
        print("Existing templates:\n"+ "\t".join(template_list()))
    else:
        target, template_type = parse()
        if os.path.exists(target):
            print("The file \"{}\" already exists!".format(target))
        else:
            try:
                with open(os.path.join(os.path.dirname(__file__),"templates/" + template_type + ".yaml"), 'r') as source:
                    run_output(target,template_type,yaml.load(source))
            except FileNotFoundError:
                print("The template \"{}\" does not exist! The possible template names are:\n".format(template_type)+ "\t".join(template_list()))
