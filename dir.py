import os

def truncated_files(rel_path):
    return ["".join(s.split(".")[:-1]) for s in os.listdir(os.path.join(os.path.dirname(__file__),rel_path))]

def rpath(rel_path):
    return os.path.join(os.path.dirname(__file__),rel_path)
def filestring(rel_path):
    return open(os.path.join(os.path.dirname(__file__),rel_path)).read()

