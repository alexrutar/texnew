# in script: check that target exists
    # print("Error: The file \"{}\" already exists. Please choose another filename.".format(target))
# must specify user file
    # print("Warning: user info file could not be found at 'user.yaml' or at 'user_private.yaml'."), and pass false, if they don't exist
    # check for user file first, raise warning if did not fine
import os
import sys

from .template import build, update, load_template, load_user, available_templates
from .document import TexnewDocument
from .error import TexnewFileError, TexnewInputError
from .file import get_version, get_name

# TODO: have defaults file in .texnew/defaults
def run(fname, template_type):
    # load and catch basic errors with template choice
    if os.path.exists(fname):
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(fname))
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
            print("The template \"{}\" does not exist! The possible template names are:\n".format(e.context_info['type'])+ "\t".join(available_templates()))
        else:
            print("uhh unknown error report this")
        sys.exit(1)

    try:
        tdoc = build(template_data, user_info)
        tdoc.write(fname)

    # TODO: improve error handling
    except TexnewFileError as e:
        print(e)
        sys.exit(1)
    except TexnewInputError as e:
        print(e)
        sys.exit(1)

#  def update(tdoc, template_type, transfer=['file-specific preamble', 'document start']):
# TODO: add error handling here
def run_update(fname, template_type):
    # basic checks
    if not os.path.exists(fname):
        print("Error: No file named \"{}\" to update!".format(fname))
        sys.exit(1)
    ver = get_version(fname)
    if ver.startswith("0."):
        print("Error: File too outdated! Must be generated with version at least 1.0; file version is ({})".format(ver))
        sys.exit(1)

    # load the document
    tdoc = TexnewDocument()
    tdoc.load(fname)

    # generate replacement document
    new_tdoc = update(tdoc, template_type)

    # copy the existing file to a new location
    name = get_name(fname,"_old")
    os.rename(fname,name)

    new_tdoc.write(fname)
