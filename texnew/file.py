import os
import yaml
import re
from pathlib import Path

class RPath:
    """Encode core directories"""
    @staticmethod
    def texnew():
        return Path.home() / '.texnew'

    @staticmethod
    def workspace():
        return Path.home() / '.texnew' / '.workspace'

    @staticmethod
    def templates():
        return Path.home() / '.texnew' / 'templates'

def read_yaml(path):
    return yaml.safe_load(path.read_text())

# clean the workspace
def clean_workspace():
    for p in RPath.workspace().iterdir():
        if not p.name == ".gitignore":
            p.unlink()


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
