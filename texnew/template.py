from .rpath import RPath
from .document import TexnewDocument


def available_templates():
    """
        **Get Available Templates**
        Create a dictionary of available templates.
    The keys in the dictionary are the names of the available packages, and each value is a list of templates which use that package.
    """
    return {d.name:[s.stem for s in d.iterdir()] for d in RPath.templates().iterdir() if d.is_dir()}


def load_template(package, tname):
    """
        **Load Template Data**
    """
    return (RPath.templates() / package / (tname + '.yaml')).read_yaml()


def load_user(order=['private','default']):
    """Load user information for sub_list"""
    for path in [(RPath.texnew() / 'user' / (a+".yaml")) for a in order]:
        if path.exists():
            return path.read_yaml()
    raise FileNotFoundError('Could not find user file!')


def build(data):
    """
        Build a New TexnewDocument.

        Build a TexnewDocument from existing data.

        :return: TexnewDocument object.

        - Example::
            
            data = ...
            build(data)

    """
    tdoc = TexnewDocument({}, sub_list=data['substitutions'])

    # set default header
    tdoc['header'] = None

    # default components
    for name in data['info']['defaults']:
        tdoc[name] = (data['root'] / "defaults" / (name + ".tex")).read_text()

    # special macros
    for name in data['macros']:
        tdoc['macros ({})'.format(name)] = (data['root'] / "macros" / (name + ".tex")).read_text()
    
    # (space for) user preamble
    tdoc['file-specific preamble'] =  None

    # file constants
    constants = (data['root'] / "formatting" / (data['formatting']+ "_constants.tex"))
    if constants.exists():
        tdoc['constants'] = constants.read_text()
    else:
        tdoc['constants'] = None

    # formatting
    tdoc['formatting'] = (data['root'] / "formatting" / (data['formatting']+ ".tex")).read_text()

    # user space
    tdoc['main document'] = (data['root'] / "contents" / (data['contents']+ ".tex")).read_text()

    return tdoc


def update(tdoc, data, transfer):
    """Update a template document with a new template type, preserving the blocks specified in the 'transfer' list"""
    new_tdoc = build(data)

    # write information to new document
    for bname in transfer:
        new_tdoc[bname] = tdoc[bname]

    # transfer constants
    old_constants = tdoc.get_constants()
    new_tdoc.set_constants(old_constants)

    return new_tdoc
