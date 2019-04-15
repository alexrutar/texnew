import sys

from .template import build, update, load_template, load_user, available_templates
from .document import TexnewDocument
from .rpath import RPath

def load_info(template_type):
    """Load template and user information simultaneously, with error handling."""
    try:
        data = load_template(template_type)
        if 'substitutions' not in data.keys():
            data['substitutions'] = {}
    except FileNotFoundError:
        print("Error: The template \"{}\" does not exist. The possible template names are:\n".format(template_type)+ "\t".join(available_templates()))
        sys.exit(1)

    try:
        user = load_user()
    except FileNotFoundError:
        print("Warning: no user file found.")
        user_info = {}

    data['substitutions'].update(user)
    return data


def run(fname, template_type):
    """Make a LaTeX file fname from template name template_type"""
    # load and catch basic errors with template choice
    fpath = RPath(fname)
    if fpath.exists():
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(fname))
        sys.exit(1)

    template_data = load_info(template_type)

    try:
        # update substitutions
        tdoc = build(template_data)
        tdoc.write(fpath)

    # TODO: this is pretty funny
    except Exception as e:
        print(e)
        sys.exit(1)


# TODO: add error handling here
def run_update(fname, template_type, transfer=['file-specific preamble', 'main document']):
    """Update given fname to new template_type, preserving blocks in transfer"""
    # basic checks
    fpath = RPath(fname)
    if not fpath.exists():
        print("Error: No file named \"{}\" to update.".format(fname))
        sys.exit(1)

    # load the document
    tdoc = TexnewDocument.load(fpath)

    # generate replacement document
    template_data = load_info(template_type)
    new_tdoc = update(tdoc, template_data, transfer)

    # copy the existing file to a new location
    fpath.safe_rename()

    new_tdoc.write(fpath)


# TODO: catch if .workspace doesn't exist for some reason?
def run_check(*targets, run_all=False):
    """Compile and test every template"""
    if run_all:
        targets = available_templates()
    for tm in targets:
        tdoc = build(load_info(tm))
        errors = tdoc.verify()
        if not errors:
            print("No errors in template '{}'".format(tm))
        else:
            print("Errors in template '{}'.".format(tm))
