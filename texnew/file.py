import os
import yaml
import re
from os.path import expanduser

from . import __path__
from .error import TexnewFileError, TexnewInputError

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
            if method == "str":
                return f.read()
            elif method == "yaml":
                return yaml.safe_load(f)
            elif method == "lst":
                return list(f)
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

# clean the workspace
def clean_workspace():
    for fl in get_flist(".workspace"):
        if not fl.startswith("."):
            os.remove(rpath(".workspace",fl))

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
