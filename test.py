from file_mgr import truncated_files, rpath, clean_dir, copy_file
import subprocess
import os
from core import texnew_run

dirname = os.path.dirname(__file__)
def parse_errors(filename):
    dct = {'errors':[],'warnings':[],'fatal':[]}
    # currently doesn't catch warnings
    with open(rpath(filename + ".log")) as f:
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

def is_empty(dct):
    for key in dct.keys():
        if dct[key]:
            return False
    return True

def run_test():
    clean_dir("log")
    for tm in truncated_files("templates"):
        # build the template in "test"
        texnew_run(rpath("test","test.tex"), tm)

        # compile the template
        lmk_args = [
                'latexmk',
                '-pdf',
                '-interaction=nonstopmode',
                '-outdir={}'.format(rpath("test")),
                rpath("test","test.tex")]
        p2 = subprocess.Popen(lmk_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p2.wait()

        # parse for errors, print errors if they exist
        e = parse_errors("test/test")
        if is_empty(e):
            print("No errors in template '{}'".format(tm))
        else:
            print("Errors in template '{}'; .tex file can be found in the log folder at '{}'.".format(tm,rpath("log")))
            copy_file(rpath("test","test.tex"),rpath("log","{}.tex".format(tm)))
            copy_file(rpath("test","test.log"),rpath("log","{}.log".format(tm)))

        # clean up
        clean_dir("test")
