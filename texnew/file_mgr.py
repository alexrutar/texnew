import os
import yaml
import re
from os.path import expanduser

from . import __path__
from .error import TexnewFileError

# get the relative path, from this script
def rpath(*rel_path):
    return os.path.join(expanduser("~"),".texnew",*rel_path)

# methods to open files with special error handling
def read_file(*rel_path, method = "lst", src = "texnew"):
    if src == "texnew":
        path = rpath(*rel_path)
    elif src == "user" and len(rel_path) == 1:
        path = rel_path[0]

    if method == "yaml":
        path += ".yaml"
    try:
        with open(path,'r') as f:
            if method == "lst":
                return lst(f)
            elif method == "str":
                return f.read()
            elif method == "yaml":
                return yaml.load(f)
    except FileNotFoundError:
        if src == "texnew":
            raise TexnewFileError(path)
        elif src == "user":
            raise TexnewInputError(path)

# method to get internal list of directories
def get_flist(*rel_path):
    path = rpath(*rel_path)
    try:
        return os.listdir(path)
    except FileNotFoundError:
        e = TexnewFileError(path)
        e.context = "directory"
        raise e

# check for file version
def get_version(filename):
    st = read_file(filename, method = "str", src = "user")
    pat = re.compile(r"% version \((.*)\)")
    res = pat.search(st)
    if res:
        return res.group(1)
    else:
        return "0.1"

# create a new block divider
def get_div(name):
    return ("% " + name + " ").ljust(80, "-") + "\n"

# remove the file endings at rel_path
def truncated_files(*rel_path):
    return ["".join(s.split(".")[:-1]) for s in get_flist(*rel_path)]

# clean the directory at a relative path
def clean_dir(*rel_path):
    for fl in get_flist(*rel_path):
        if not fl.startswith("."):
            os.remove(rpath(*rel_path,fl))

# copy a file to the target; only appends, does not overwrite
def copy_file(src,trg):
    with open(src,'r') as f, open(trg,'a+') as output:
        for l in f:
            output.write(l)

# get an available name, inserting 'ad' if necessary
def get_name(name,ad):
    if "." in name:
        base = "".join(name.split(".")[:-1])
        ftype = name.split(".")[-1]
    else:
        base = name
        ftype = ""
    for t in [""] + ["_"+str(x) for x in range(1000)]:
        attempt = base + ad + t + "." + ftype
        if not os.path.exists(attempt):
            return attempt

# check if a string is a divider (with any name)
def is_div(st):
    dv = get_div("")
    return len(st) == len(dv) and st.startswith(dv[:2]) and st.endswith(dv[-3:])

# separate a block named div_name
def sep_block(lst, div_name):
    start = get_div(div_name)
    read = False
    id1 = None
    id2 = None
    for e,l in enumerate(lst):
        if read and is_div(l):
            id2 = e
            break
        if l == start:
            id1 = e+1
            read = True
    if id1 is None:
        return []
    if id2 is None:
        return lst[id1:]
    return lst[id1:id2]
