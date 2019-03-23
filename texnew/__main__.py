"""
Entry point for the texnew script installed along with this package.



    texnew [-uv] target template

    banditvis [-cl]
    banditvis -h | --help
    banditvis -V | --version

Positional:
  target                The name of the file to action.
  template              The name of the template to use.

Optional:
  -u                    Update the target template with the given file.
  -v                    Run verbose.

Other:
  -c                    Check existing templates for errors.
  -l                    List existing templates.

"""
import sys
import argparse

from . import __version__
from .test import test
from .core import run
from .file_mgr import truncated_files
from .update import update as texnew_update

def get_usage():
    return '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
# main argument parser, after pre-checking info
def parse():
    parser = argparse.ArgumentParser(prog="texnew",description='An automatic LaTeX template creator and manager.',usage=get_usage())
    parser.add_argument('target', metavar='output', type=str, nargs=1,
                                help='the name of the file you want to create')
    parser.add_argument('template_type', metavar='template', type=str, nargs=1,
                                help='the name of the template to use')

    parser.add_argument('-l', "--list", action="store_true", default=False, dest="lst",help="list existing templates and root folder")
    parser.add_argument('-c', "--check", action="store_true", default=False, dest="lst",help="check for errors in existing templates")
    parser.add_argument('-u', "--update", action="store_true", default=False, dest="update",help="update the specified file with the desired template")

    args = parser.parse_args()
    return (args.target[0], args.template_type[0], args.update)

def main():
    # special use cases:
    if ("-h"  in sys.argv[1:]) or ("--help" in sys.argv[1:]) or (len(sys.argv) == 1):
        print(get_usage())
    elif "-V" in sys.argv[1:] or "--version" in sys.argv[1:]:
        print("texnew ({})".format(__version__))
    elif "-l" in sys.argv[1:]:
        print("\nRoot Folder: {}/".format(rpath()))
        print("Existing templates:\n"+ "\t".join(truncated_files("share","templates")))
    elif "-c" in sys.argv[1:]:
        test()
    else:
        target, template_type, update = parse()
        if update:
            texnew_update(target, template_type)
        else:
            if not target.endswith(".tex"):
                target = target + ".tex"
            run(target, template_type)

# entry point for script
if __name__ == "__main__":
    main()
