import os

def truncated_files(rel_path):
    return ["".join(s.split(".")[:-1]) for s in os.listdir(os.path.join(os.path.dirname(__file__),rel_path))]
def rpath(*rel_path):
    return os.path.join(os.path.dirname(__file__),*rel_path)
def clean_dir(*rel_path):
    for fl in os.listdir(rpath(*rel_path)):
        os.remove(rpath(*rel_path,fl))
def filestring(*rel_path):
    with open(rpath(*rel_path)) as f:
        out = f.read()
    return out

def copy_file(src,trg):
    with open(src,'r') as f, open(trg,'a+') as output:
        for l in f:
            output.write(l)

def lsplit(lst, start_cond, end_cond):
    out = []
    read = False
    temp = []
    for l in lst:
        if read and end_cond(l):
            read = False
            out += [temp]
        if start_cond(l):
            read = True
            temp = []
        if read:
            temp += [l]
    if read:
        out += [temp]
    return out
