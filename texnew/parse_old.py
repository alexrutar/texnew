
def parse_old():
    """Main argument parser"""
    parser = argparse.ArgumentParser(prog="texnew",description='An automatic LaTeX template creator and manager.',usage="")

    # main arguments
    parser.add_argument('target',
            metavar='output',
            type=str, nargs=1,
            help='the name of the file you want to create')
    parser.add_argument('template_type',
            metavar='template',
            type=str,
            nargs=1,
            help='the name of the template to use')

    # optional arguments
    parser.add_argument('-l', "--list",
            action="store_true",
            default=False,
            dest="lst",
            help="list existing templates and root folder")
    parser.add_argument('-c', "--check",
            action="store_true",
            default=False,
            dest="check",
            help="check for errors in existing templates")
    parser.add_argument('-u', "--update_file",
            action="store_true",
            default=False,
            dest="update",
            help="update the specified file with the desired template")
    parser.add_argument("--keep-formatting",
            dest="transfer",
            action="store_true",
            default=False,
            help="preserve formatting options")

    return parser.parse_args()
    #  return (args.target[0], args.template_type[0], args.update_file, args.transfer)


class Launcher:
    transfer=['file-specific preamble', 'main document']

    def __init__(self):
        pass

    def initialize_args(self):
        self.args = parse()

    def launch(self):
        if self.args.update:
            self.update()
        else:
            self.run()
    # checking methods
    def check(self):
        checklist = {'no rpath': (RPath.texnew().exists(), "Missing template information at '{}'".format(RPath.texnew()))}
        for k,(check,val) in checklist.items():
            if not check:
                print(val)

    # override methods
    def override_args(self):
        args = {'-h': self.help,
                '--help': self.help,
                '-V': self.version,
                '--version': self.version,
                '-l': self.list,
                '--list': self.list,
                '-c': self.test,
                '--check': self.test}
        args[sys.argv[1]]()

    def help(self):
        print('\n\n\n'.join(__doc__.split('\n\n\n')[1:]))
    def version(self):
        print("texnew ({})".format(__version__))
    def list(self):
        print("Existing templates:\n"+ "\t".join(available_templates()))
    def test(self):
        run_test()

    # main methods
    def update(self):
        if self.args.transfer:
            self.transfer.append('formatting')
        run_update(self.args.target[0], self.args.template_type[0], transfer=self.transfer)

    def run(self):
        if not self.args.target[0].endswith(".tex"):
            self.args.target[0] += ".tex"
        run(self.args.target[0], self.args.template_type[0])
