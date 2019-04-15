import sys
import argparse

from .scripts import run, run_update, run_check
from .template import available_templates
from .rpath import RPath
from . import __version__, __repo__

def _tn(args):
    """Wrapper for scripts.run"""
    if not args.output[0].endswith(".tex"):
        args.output[0] += ".tex"
    run(args.output[0], args.template[0])

def _tn_update(args):
    """Wrapper for scripts.run_update"""
    if args.format:
        args.transfer.extend(['formatting','doctype'])
    run_update(args.target[0], args.template[0], transfer=args.transfer)

def _tn_check(args):
    """Wrapper for scripts.run_check"""
    run_check(*args.names,run_all=args.all)

def _tn_info(args):
    """Print basic repository information."""
    msg = {'lst':"Existing templates:\n"+ "\t".join(available_templates()),
            'dir':'Root directory: {}'.format(RPath.texnew())}
    d = vars(args)
    print("Repository location: {}".format(__repo__))
    for k in msg.keys():
        if d[k]:
            print(msg[k])


def parse_errors(args):
    """Catch basic errors"""
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
    parser_main.set_defaults(func=_tn)
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
    parser_update.set_defaults(func=_tn_update)
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
    parser_check.set_defaults(func=_tn_check)
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
    parser_info.set_defaults(func=_tn_info)
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
