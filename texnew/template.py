from .rpath import RPath
from .document import TexnewDocument


def available_templates():
    """Print available templates"""
    return {d.name:[s.stem for s in d.iterdir()] for d in RPath.templates().iterdir() if d.is_dir()}


def load_template(package,template_name):
    """Load template information for template_data"""
    return (RPath.templates() / package / (template_name + '.yaml')).read_yaml()


def load_user(order=['private','default']):
    """Load user information for sub_list"""
    for path in [(RPath.texnew() / 'user' / (a+".yaml")) for a in order]:
        if path.exists():
            return path.read_yaml()
    raise FileNotFoundError('Could not find user file!')


def build(template_data, defaults=['doctype','packages','macros']):
    """Build a TexnewDocument from existing template_data."""
    tdoc = TexnewDocument({}, sub_list=template_data['substitutions'])

    # set default header
    tdoc['header'] = None

    # default components
    for name in template_data['info']['defaults']:
        tdoc[name] = (template_data['root'] / "defaults" / (name + ".tex")).read_text()

    # special macros
    for name in template_data['macros']:
        tdoc['macros ({})'.format(name)] = (template_data['root'] / "macros" / (name + ".tex")).read_text()
    
    # (space for) user preamble
    tdoc['file-specific preamble'] =  None

    # file constants
    constants = (template_data['root'] / "formatting" / (template_data['formatting']+ "_constants.tex"))
    if constants.exists():
        tdoc['constants'] = constants.read_text()
    else:
        tdoc['constants'] = None

    # formatting
    tdoc['formatting'] = (template_data['root'] / "formatting" / (template_data['formatting']+ ".tex")).read_text()

    # user space
    tdoc['main document'] = (template_data['root'] / "contents" / (template_data['contents']+ ".tex")).read_text()

    return tdoc


def update(tdoc, template_data, transfer):
    """Update a template document with a new template type, preserving the blocks specified in the 'transfer' list"""
    new_tdoc = build(template_data)

    # write information to new document
    for bname in transfer:
        new_tdoc[bname] = tdoc[bname]

    # transfer constants
    old_constants = tdoc.get_constants()
    new_tdoc.set_constants(old_constants)

    return new_tdoc
