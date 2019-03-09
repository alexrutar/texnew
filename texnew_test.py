from dir import truncated_files
import subprocess
import os

filename = "test"

def parse_errors(filename):
    dct = {'errors':[],'warnings':[],'fatal':[]}
    # currently doesn't catch warnings
    with open(filename + ".log") as f:
        append = False
        for l in f:
            if l.startswith("! "):
                dct['fatal'] += [l]
            if l.startswith("./" + filename + ".tex:"):
                temp = ""
                append = True
            if append:
                temp += l
            if l.startswith("l."):
                append = False
                dct['errors'] += [temp]
        dct['errors'] += [l.strip()]
    return dct

def empty(dct):
    for key in dct.keys():
        if dct[key] != []:
            return False
    return True

def run_autogen():
    templates = truncated_files("templates")
    for tm in templates:
        p1 = subprocess.Popen(["python3","texnew.py","test/test.tex",tm])
        p1.wait()
        args = ['latexmk','-pdf', '-jobname=test/test',"test/test.tex"]
        p2 = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p2.wait()

        e = parse_errors("test/test.log")
        if empty(e):
            print("No errors in template '{}'".format(tm))
        else:
            for key in e.keys():
                print("{}:".format(key))
                for error in e[key]:
                    print(error)
        for fl in os.listdir("test"):
            fpath = os.path.join("test", fl)
            os.remove(fpath)
    print(templates)
    # get template list
    # for each template:
    #   compile it, check log for errors
    #   if errors, print error messages along with line
if __name__ == "__main__":
    run_autogen()
