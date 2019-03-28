
# in script: check that target exists
    # print("Error: The file \"{}\" already exists. Please choose another filename.".format(target))
# must specify user file
    # print("Warning: user info file could not be found at 'user.yaml' or at 'user_private.yaml'."), and pass false, if they don't exist
    # check for user file first, raise warning if did not fine

import os
import sys
from .core import run as run_texnew
from .core import load_template, load_user
from .file_mgr import read_file, truncated_files
from .error import TexnewFileError, TexnewInputError

# have defaults file in .texnew/defaults
def run(target, template_type, user_macros={}):
    # load and catch basic errors with template choice
    if os.path.exists(target):
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(target))
        sys.exit(1)

    try:
        user_info = load_user("private")
    except TexnewFileError:
        try:
            user_info = load_user()
        except TexnewFileError as e:
            print("Warning: no user file found, no substitutions will be made!")
            user_info = {}

    try:
        template_data = load_template(template_type)
    except TexnewFileError as e:
        if e.context == "template":
            print("The template \"{}\" does not exist! The possible template names are:\n".format(e.context_info['type'])+ "\t".join(truncated_files("templates")))
        else:
            print("uhh unknown error report this")
        sys.exit(1)

    try:
        test = run_texnew(template_data, user_info, user_macros)
        with open(target, "a+") as f:
            f.write(test.gen_file())

    except TexnewFileError as e:
        print(e)
        sys.exit(1)
    except TexnewInputError as e:
        print(e)
        sys.exit(1)
