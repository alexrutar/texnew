from .file import RPath, read_yaml
from .document import TexnewDocument

def load_template(template_type):
    """Load template information for template_data"""
    return read_yaml(RPath.templates() / (template_type + '.yaml'))

# TODO: use PATH, replace get_flist
def available_templates():
    return [s.stem for s in RPath.templates().iterdir()]

def load_user(order=['private','default']):
    """Load user information for sub_list"""
    for path in [(RPath.texnew() / 'user' / (a+".yaml")) for a in order]:
        if path.exists():
            return read_yaml(path)
    raise FileNotFoundError('Could not find user file!')

def build(template_data, sub_list={}):
    """Build a TexnewDocument from existing template_data.
    Note: makes a lot of assumptions about the structure of template_data"""
    sub_list['doctype'] = template_data['doctype']
    tdoc = TexnewDocument({}, sub_list=sub_list)
    p = RPath.texnew() / 'share' / template_data['template']

    # set default header
    tdoc['header'] = None

    # default components
    tdoc['doctype'] =  (p / "defaults" / "doctype.tex").read_text()
    tdoc['packages'] =  (p / "defaults" / "packages.tex").read_text()
    tdoc['default macros'] =  (p / "defaults" / "macros.tex").read_text()

    # special macros
    for name in template_data['macros']:
        tdoc['macros ({})'.format(name)] = (p / "macros" / (name + ".tex")).read_text()
    
    # (space for) user macros
    tdoc['file-specific preamble'] =  None

    # formatting block
    tdoc['formatting'] = (p / "formatting" / (template_data['formatting']+ ".tex")).read_text()

    # user space
    tdoc['document start'] = (p / "contents" / (template_data['contents']+ ".tex")).read_text()

    return tdoc

def update(tdoc, template_type, transfer):
    # generate replacement document
    user_info = load_user()
    template_data = load_template(template_type)
    new_tdoc = build(template_data, sub_list=user_info)

    # write information to new document
    for bname in transfer:
        new_tdoc[bname] = tdoc[bname]
    return new_tdoc
