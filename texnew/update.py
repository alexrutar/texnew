import os
import re

from .file_mgr import copy_file, get_name, get_div, get_version, sep_block
from .core import run
from . import __version__


# main update function
def update(filename, template_type):
    if not os.path.exists(filename):
        print("Error: The file \"{}\" does not exist. Please choose another filename.".format(filename))
    elif get_version(filename).startswith("0."):
        print("Error: File too outdated! Must be generated with version at least 1.0; file version is ({})".format(__version__))
    else:
        # copy the file to a new location
        name = get_name(filename,"_old")
        os.rename(filename,name)

        # read contents of file to user dict by separating relevant blocks
        with open(name,'r') as f:
            fl = list(f)
        macros = sep_block(fl,"file-specific macros")
        body = sep_block(fl,"document start")

        # strip last item of macros to avoid increasing whitespace in file
        if len(macros) >= 1:
            macros[-1] = macros[-1].rstrip()

        # rebuild file
        user = {'macros':macros,'contents':body}
        run(filename, template_type, user_macros=user)
