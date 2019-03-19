# take input file
# separate input file into:
# - file macros
# - main files
# merge macros + main file with new template
# copy file to new location
# write new version of file
from file_mgr import copy_file, lsplit, get_name, get_div
from core import texnew_run
import os

def match_div(name=""):
    st = get_div(name)
    if name:
        return lambda x:x == get_div(name)
    else:
        st = get_div("")
        return lambda x:len(x) == len(st) and x.startswith(st[:2]) and x.endswith(st[-3:])

def texnew_update(filename, template_type):
    if not os.path.exists(filename):
        print("Error: The file \"{}\" does not exist. Please choose another filename.".format(filename))
    else:
        # copy the file to a new location
        name = get_name(filename,"_old")
        os.rename(filename,name)

        # read contents of file to user dict
        with open(name,'r') as f:
            fl = list(f)
        macros = lsplit(fl,match_div("file-specific macros"),match_div())[0]
        body = lsplit(fl,match_div("document start"),lambda x:False)[0]
        macros[-1] = macros[-1].rstrip()
        user = {'macros':macros,'contents':body}

        texnew_run(filename, template_type, user_macros=user)
