"""
Entry point for the texnew script installed along with this package.



    texnew [-uv] [--user=USER] target template

    texnew [-cl]
    texnew -h | --help
    texnew -V | --version

Positional:
  target                The name of the file to action.
  template              The name of the template to use.

Named:
  --user                Specify the user file to use.

Optional:
  -u                    Update the target template with the given file.
  --keep-formatting     When updating, preserve the formatting section in the file.
  -v                    Run verbose.

Other:
  -c                    Check existing templates for errors.
  -l                    List existing templates.
"""
import sys
import argparse

from . import __version__
from .scripts import run, run_update, run_test
from .template import available_templates
from .rpath import RPath

# TODO: should probably do something else (aka fix this)
def get_usage():
    return '\n\n\n'.join(__doc__.split('\n\n\n')[1:])


def parse():
    """Main argument parser"""
    parser = argparse.ArgumentParser(prog="texnew",description='An automatic LaTeX template creator and manager.',usage=get_usage())
    parser.add_argument('target', metavar='output', type=str, nargs=1,
                                help='the name of the file you want to create')
    parser.add_argument('template_type', metavar='template', type=str, nargs=1,
                                help='the name of the template to use')

    parser.add_argument('-l', "--list", action="store_true", default=False, dest="lst",help="list existing templates and root folder")
    parser.add_argument('-c', "--check", action="store_true", default=False, dest="check",help="check for errors in existing templates")
    parser.add_argument('-u', "--update_file", action="store_true", default=False, dest="update_file",help="update_file the specified file with the desired template")
    parser.add_argument("--user", dest="user", default="",help="specify the user file",nargs=1)
    parser.add_argument("--keep-formatting", dest="transfer", action="store_true", default=False, help="specify the user file")

    args = parser.parse_args()
    # TODO: don't pass like this, just pass args, figure out why some need [0]
    return (args.target[0], args.template_type[0], args.update_file, args.user, args.transfer)


def main():
    """Script entry point"""
    if ("-h"  in sys.argv[1:]) or ("--help" in sys.argv[1:]) or (len(sys.argv) == 1):
        print(get_usage())
    elif "-V" in sys.argv[1:] or "--version" in sys.argv[1:]:
        print("texnew ({})".format(__version__))
    elif "-l" in sys.argv[1:]:
        print("\nRoot Folder: {}/".format(RPath.texnew()))
        print("Existing templates:\n"+ "\t".join(available_templates()))
    elif "-c" in sys.argv[1:]:
        run_test()
    else:
        # main program branching
        target, template_type, update_file, user, tr = parse()
        transfer=['file-specific preamble', 'main document']
        if tr:
            transfer.append('formatting')
        if update_file:
            run_update(target, template_type, transfer=transfer)
        else:
            if not target.endswith(".tex"):
                target = target + ".tex"
            run(target, template_type)


if __name__ == "__main__":
    main()
