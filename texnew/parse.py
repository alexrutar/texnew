"""
Entry point for the texnew script installed along with this package.



    texnew [-uv] target template

    texnew [-cl]
    texnew -h | --help
    texnew -V | --version

Positional:
  target                The name of the file to action.
  template              The name of the template to use.

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

from .scripts import run, run_update, run_check
from .template import available_templates
from .rpath import RPath
from . import __version__

def tn(args):
    if not args.output[0].endswith(".tex"):
        args.output[0] += ".tex"
    run(args.output[0], args.template[0])

def tn_update(args):
    if args.format:
        args.transfer.extend(['formatting','doctype'])
    run_update(args.target[0], args.template[0], transfer=args.transfer)

def tn_check(args):
    run_check(args.names,run_all=args.all)

def tn_info(args):
    # TODO
    # point to installation location
    # have listing option
    msg = {'lst':"Existing templates:\n"+ "\t".join(available_templates()),
            'dir':'Root directory: {}'.format(RPath.texnew())}
    d = vars(args)
    for k in msg.keys():
        if d[k]:
            print(msg[k])


def parse_errors(args):
    checklist = {'texnew_exists': (RPath.texnew().exists(), "Missing template information at '{}'".format(RPath.texnew())),
            'texnew_workspace_exists': (RPath.workspace().exists(), "Missing workspace directory at '{}'".format(RPath.workspace()))}
    for k,(check,val) in checklist.items():
        if not check:
            print("Error: ", val)

def main():
    """Main argument parser"""
    parser = argparse.ArgumentParser(prog="texnew",description='An automatic LaTeX template creator and manager.')
    parser.add_argument('-v','--verbose',
            action='store_true',
            default=False,
            dest='verbose',
            help='run verbose mode')
    parser.add_argument('--version',
            action='version',
            version='%(prog)s {}'.format(__version__))
    subparsers = parser.add_subparsers(help="test")

    # main arguments
    parser_main = subparsers.add_parser('new', help='create a new template')
    parser_main.set_defaults(func=tn)
    parser_main.add_argument('output',
            type=str,
            nargs=1,
            help='the name of the file you want to create')
    parser_main.add_argument('template',
            type=str,
            nargs=1,
            help='the name of the template to use')

    # update arguments
    parser_update = subparsers.add_parser('update', help='update an existing file')
    parser_update.set_defaults(func=tn_update)
    parser_update.add_argument('target',
            type=str,
            nargs=1,
            help='the name of the file to update')
    parser_update.add_argument('template',
            type=str,
            nargs=1,
            help='the name of the template to update with')
    parser_update.add_argument("-f","--keep-formatting",
            dest="format",
            action="store_true",
            default=False,
            help="preserve the formatting block")
    parser_update.add_argument("-t","--transfer",
            nargs="*",
            default=['file-specific preamble', 'main document'],
            help="provide a list of blocks to transfer")

    # check arguments
    parser_check = subparsers.add_parser('check', help='check templates for errors')
    parser_check.set_defaults(func=tn_check)
    parser_check.add_argument('names',
            nargs="*",
            default=False,
            help="check all existing templates for errors")
    parser_check.add_argument('-a', "--all",
            action="store_true",
            default=False,
            dest="all",
            help="check all existing templates for errors")

    # info arguments
    parser_info = subparsers.add_parser('info', help='print information about the parser')
    parser_info.set_defaults(func=tn_info)
    parser_info.add_argument('-l', "--list",
            action="store_true",
            default=False,
            dest="lst",
            help="list existing templates")
    parser_info.add_argument('-d', "--directory",
            action="store_true",
            default=False,
            dest="dir",
            help="display path to the root folder")

    args = parser.parse_args()
    parse_errors(args)

    args.func(args)
