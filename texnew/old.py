

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
def run(target,data,sub_list={},user_macros={}):
    tex_doctype = re.sub(repl_match("doctype"), data['doctype'], read_file("share","defaults","doctype.tex",method="str"))
    tex_packages = read_file("share","defaults","packages.tex",method="str")
    tex_macros = read_file("share","defaults","macros.tex",method="str")
    tex_formatting = read_file("share","formatting",data['formatting'] + '.tex',method="str")
    
    # substitute sub_list
    for k in sub_list.keys():
        tex_formatting = re.sub(repl_match(k), str(sub_list[k]), tex_formatting)

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
