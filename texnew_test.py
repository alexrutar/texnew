from dir import truncated_files
import subprocess
import os

dirname = os.path.dirname(__file__)
def parse_errors(filename):
    dct = {'errors':[],'warnings':[],'fatal':[]}
    # currently doesn't catch warnings
    with open(os.path.join(dirname,filename + ".log")) as f:
        append = False
        temp = ""
        for l in f:
            if l.startswith("! "):
                dct['fatal'] += [l]
            if l.startswith("./" + filename + ".tex:"):
                temp = l
                append = True
            if append:
                temp += l
            if l.startswith("l."):
                temp += l
                append = False
                dct['errors'] += [temp]
    return dct

def empty(dct):
    for key in dct.keys():
        if dct[key]:
            return False
    return True

def run_test():
    for fl in os.listdir(os.path.join(dirname,"log")):
        fpath = os.path.join(dirname,os.path.join("log", fl))
        os.remove(fpath)

    templates = truncated_files("templates")
    for tm in templates:
        fl = os.path.join(dirname,"test")
        fl_tex = fl + "/test.tex"
        p1 = subprocess.Popen(["python3",os.path.join(dirname,"texnew.py"),fl_tex,tm])
        p1.wait()
        args = ['latexmk','-pdf', '-interaction=nonstopmode', '-outdir={}'.format(fl),fl_tex]
        p2 = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p2.wait()
        e = parse_errors("test/test")
        if empty(e):
            print("No errors in template '{}'".format(tm))
        else:
            print("Errors in template '{}'; .tex file can be found in the log folder.".format(tm))
            with open(os.path.join(dirname,"test/test.tex"),'r') as f, open(os.path.join(dirname,"log/{}.tex".format(tm)),'w+') as output:
                for l in f:
                    output.write(l)
        for fl in os.listdir(os.path.join(dirname,"test")):
            fpath = os.path.join(dirname,os.path.join("test", fl))
            os.remove(fpath)
