import re

from .file import read_file, truncated_files
from .error import TexnewFileError
from .document import TexnewDocument

def load_template(template_type):
    """Load template information for template_data"""
    try:
        return read_file("templates",template_type,method="yaml")
    except TexnewFileError as e:
        e.context = "template"
        e.context_info['type'] = template_type
        raise e

# TODO: write this function
def available_templates():
    return truncated_files("templates")

def load_user(info_name = "default"):
    """Load user information for sub_list"""
    try:
        return read_file("user",info_name,method="yaml")
    except TexnewFileError as e:
        e.context = "user"
        e.context_info['name'] = info_name
        raise e

def build(template_data, sub_list={}):
    """Build a TexnewDocument from existing template_data.
    Note: makes a lot of assumptions about the structure of template_data"""
    sub_list['doctype'] = template_data['doctype']
    tdoc = TexnewDocument(sub_list)
    rel = ['share', template_data['template']]

    # set default header
    tdoc['header'] = None

    # default components
    tdoc['doctype'] =  read_file(*rel,"defaults","doctype.tex")
    tdoc['packages'] =  read_file(*rel,"defaults","packages.tex")
    tdoc['default macros'] =  read_file(*rel,"defaults","macros.tex")

    # special macros
    for name in template_data['macros']:
        tdoc['macros ({})'.format(name)] = read_file(*rel,"macros",name + ".tex")
    
    # add existing user macros
    tdoc['file-specific preamble'] =  None

    # formatting block
    tdoc['formatting'] = read_file(*rel,"formatting",template_data['formatting']+ ".tex")

    # add existing user contents
    tdoc['document start'] = None

    return tdoc

def update(tdoc, template_type, transfer=['file-specific preamble', 'document start']):
    # generate replacement document
    user_info = load_user()
    template_data = load_template(template_type)
    new_tdoc = build(template_data, sub_list=user_info)

    # write information to new document
    for bname in transfer:
        new_tdoc[bname] = tdoc[bname]

    return new_tdoc
