import subprocess
import os

from .core import run
from .file_mgr import truncated_files, rpath, clean_dir, copy_file

# parse the file for errors
# TODO: this is garbage, fix it
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

# check if a dct has any non-empty lists
def is_empty(dct):
    for key in dct.keys():
        if dct[key]:
            return False
    return True

# run the test
def test():
    # clean log/test directory
    clean_dir("log")
    clean_dir("test")

    # iterate over possible template names
    for tm in truncated_files("share","templates"):
        # build the template in "test"
        run(rpath("test","test.tex"), tm)

        # compile the template
        lmk_args = [
                'latexmk',
                '-pdf',
                '-interaction=nonstopmode',
                '-outdir={}'.format(rpath("test")),
                rpath("test","test.tex")]
        p2 = subprocess.Popen(lmk_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # TODO: not good to suppress errors
        p2.wait()

        # parse for errors, print errors if they exist
        e = parse_errors("test/test")
        if is_empty(e):
            print("No errors in template '{}'".format(tm))
        else:
            # if there are errors, we copy the relevant files to the log folder
            print("Errors in template '{}'; .tex file can be found in the log folder at '{}'.".format(tm,rpath("log")))
            copy_file(rpath("test","test.tex"),rpath("log",tm + ".tex"))
            copy_file(rpath("test","test.log"),rpath("log",tm + ".log"))

        # clean up
        clean_dir("test")
