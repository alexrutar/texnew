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

def truncated_files(rel_path):
    return ["".join(s.split(".")[:-1]) for s in os.listdir(os.path.join(os.path.dirname(__file__),rel_path))]

def print_detailed_info():
    print("\nRoot Folder: {}/".format(os.path.dirname(__file__)))
    print("   All other file paths are relative to this folder.")

    print("\nUser Info: src/user.yaml")
    print("   Input custom user data here; see Formatting")

    print("\nTemplates: templates")
    print("   Define new templates in the existing style. There are three (mandatory) options. 'doctype' can be any valid LaTeX document type (e.g. article, book). 'formatting' must be any filename (without extension) defined in Formatting. 'macros' must be any filename (without extension) defined in Macros.")

    print("\nMacros: src/macros")
    print("  Macro files stored here are accessed by the 'macro' option in the templates")

    print("\nFormatting: src/formatting")
    print("   Formatting files stored here are accessed by the 'formatting' option in the templates. They must include '\\begin{document}' and '\\end{document}'. Whever '<+key+>' appears in a formatting document, they are automatically replaced by the relevant info in the 'user.yaml' file. You can define new keys.")


def parse():
    parser = argparse.ArgumentParser(prog="texnew",description='An automatic LaTeX template creator.')
    parser.add_argument('target', metavar='output', type=str, nargs=1,
                                help='the name of the file you want to create')
    parser.add_argument('template_type', metavar='template', type=str, nargs=1,
                                help='the name of the template to use')

    parser.add_argument('-l', "--list", action="store_true", default=False, dest="lst",help="list existing templates")
    parser.add_argument('-i', "--info", action="store_true", default=False, dest="lst",help="display detailed info about template sources")

    args = parser.parse_args()
    target = args.target[0]
    if not target.endswith(".tex"):
        target = target + ".tex"
    template_type = args.template_type[0]
    truncated_files("templates")

    return (target, template_type)


def run_output(target,template_type,data,user_info):
    tex_doctype = re.sub(repl_match("doctype"), data['doctype'], filestring("src/defaults/doctype.tex"))
    tex_packages = filestring("src/defaults/packages.tex")
    tex_macros = filestring("src/defaults/macros.tex")
    tex_formatting = filestring("src/formatting/" + data['formatting'] + '.tex')
    for k in user_info.keys():
        tex_formatting = re.sub(repl_match(k), user_info[k], tex_formatting)

    with open(target,"a+") as output:
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
            output.write(filestring("src/macros/" + name + ".tex"))

        # add formatting file
        write_div(output, "formatting")
        output.write(tex_formatting)

if __name__ == "__main__":
    if "-l" in sys.argv:
        print("Existing templates:\n"+ "\t".join(truncated_files("templates")))
    elif "-i" in sys.argv:
        print_detailed_info()
    else:
        target, template_type = parse()
        if os.path.exists(target):
            print("The file \"{}\" already exists!".format(target))
        else:
            try:
                with open(os.path.join(os.path.dirname(__file__),"templates/" + template_type + ".yaml"), 'r') as source, open(os.path.join(os.path.dirname(__file__),"src/user.yaml"), 'r') as user_info:
                    data = yaml.load(source)
                    user_info = yaml.load(user_info)
                run_output(target,template_type,data,user_info)
            except FileNotFoundError:
                print("The template \"{}\" does not exist! The possible template names are:\n".format(template_type)+ "\t".join(truncated_files("templates")))
