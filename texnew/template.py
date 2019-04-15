from .rpath import RPath
from .document import TexnewDocument


def available_templates():
    """Print available templates"""
    return [s.stem for s in RPath.templates().iterdir()]


def load_template(template_type):
    """Load template information for template_data"""
    return (RPath.templates() / (template_type + '.yaml')).read_yaml()


def load_user(order=['private','default']):
    """Load user information for sub_list"""
    for path in [(RPath.texnew() / 'user' / (a+".yaml")) for a in order]:
        if path.exists():
            return path.read_yaml()
    raise FileNotFoundError('Could not find user file!')


# TODO: option to load custom defaults list from template (maybe default list should be found in the root of the template set)
def build(template_data, defaults=['doctype','packages','macros']):
    """Build a TexnewDocument from existing template_data."""
    tdoc = TexnewDocument({}, sub_list=template_data['substitutions'])
    p = RPath.texnew() / 'share' / template_data['template']

    # set default header
    tdoc['header'] = None

    # default components
    for name in defaults:
        tdoc[name] = (p / "defaults" / (name + ".tex")).read_text()

    # special macros
    for name in template_data['macros']:
        tdoc['macros ({})'.format(name)] = (p / "macros" / (name + ".tex")).read_text()
    
    # (space for) user preamble
    tdoc['file-specific preamble'] =  None

    # file constants
    constants = (p / "formatting" / (template_data['formatting']+ "_constants.tex"))
    if constants.exists():
        tdoc['constants'] = constants.read_text()
    else:
        tdoc['constants'] = None

    # formatting
    tdoc['formatting'] = (p / "formatting" / (template_data['formatting']+ ".tex")).read_text()

    # user space
    tdoc['main document'] = (p / "contents" / (template_data['contents']+ ".tex")).read_text()

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
