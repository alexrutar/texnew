import itertools
import yaml
from pathlib import Path

# TODO: potentially subclass Path here - however, I've had a hard time doing this, may need to wait for an update
# would include read_yaml, get_name, and clean_workspace() as custom methods, change staticmethod to classmethod
class RPath:
    """Stores the location of core directories"""
    @staticmethod
    def texnew():
        return Path.home() / '.texnew'

    @staticmethod
    def workspace():
        return Path.home() / '.texnew' / '.workspace'

    @staticmethod
    def templates():
        return Path.home() / '.texnew' / 'templates'


def read_yaml(path):
    """Read a yaml file pointed to by a path."""
    return yaml.safe_load(path.read_text())


def clean_workspace():
    """Deletes all files in '~/.texnew/.workspace' except .gitignore"""
    for p in RPath.workspace().iterdir():
        if not p.name == ".gitignore":
            p.unlink()


def safe_rename(path):
    """Safely rename a file pointed to by path"""
    for t in itertools.count():
        new_path = path.with_name("{}_{}".format(path.stem, t) + "".join(path.suffixes))
        if not new_path.exists():
            path.rename(new_path)
            break
