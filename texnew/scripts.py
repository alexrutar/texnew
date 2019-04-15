import sys

from .template import build, update, load_template, load_user, available_templates
from .document import TexnewDocument
from .rpath import RPath

def parse_ttype(template_type,default='base'):
    """Parse the user-specified template type."""
    out = template_type.split("-")
    if len(out) == 1:
        return (default, template_type)
    elif len(out) == 2:
        return (out[0], out[1])
    else:
        print("Error: Invalid package name '{}': contains too many hyphens".format(template_type))

def template_str():
    """Return a string representation of the existing packages and templates."""
    return "\n\n".join(["Package '{}':\n".format(d)+"  "+"\t".join(v) for d,v in available_templates().items()])

def load_data(template_type):
    """Build a data dictionary from template and user information as required by .template.build"""
    try:
        user = load_user()
    except FileNotFoundError:
        print("Warning: no user file found.")
        user = {}
    try:
        defs = user['defaults']['package']
    except KeyError:
        defs = 'base'

    package, template_name = parse_ttype(template_type,default=defs)

    try:
        data = load_template(package, template_name)
        data['package'] = package
        data['template_name'] = template_name
    except FileNotFoundError:
        print("Error: The template \"{}\" does not exist. Run `texnew info -l` for a list of templates.".format(template_type))
        sys.exit(1)

    for name in ['substitutions']:
        if name not in data.keys():
            data[name] = {}
        data[name].update(user[name])

    data['root'] = RPath.texnew() / 'packages' / package
    data['info'] = (data['root'] / "package_info.yaml").read_yaml()

    #TODO: check for errors here in the template / user info

    return data


def run(fname, template_type):
    """Make a LaTeX file fname from template name template_type"""
    fpath = RPath(fname)
    if fpath.exists():
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(fname))
        sys.exit(1)

    template_data = load_data(template_type)

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
    """Update an existing texnew document to a new template type, preserving a list of specified blocks.
    fname: the name of the file to update
    template_type: the name of the new template style
    transfer: a list of blocks to transfer
    """
    """Update given fname to new template_type, preserving blocks in transfer"""
    fpath = RPath(fname)
    if not fpath.exists():
        print("Error: No file named \"{}\" to update.".format(fname))
        sys.exit(1)

    tdoc = TexnewDocument.load(fpath)

    template_data = load_data(template_type)
    new_tdoc = update(tdoc, template_data, transfer)

    fpath.safe_rename()
    new_tdoc.write(fpath)


def run_check(*targets):
    """Test every template given as an argument for errors"""
    for tm in targets:
        data = load_data(tm)
        tdoc = build(data)
        errors = tdoc.verify()

        name = '{package}-{template_name}'.format(**data)
        if not errors:
            print("No errors in template '{}'".format(name))
        else:
            print("Errors in template '{}'.".format(name))
