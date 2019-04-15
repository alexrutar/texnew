import itertools
import yaml
import os
from pathlib import Path, PosixPath as _PosixPath_, WindowsPath  as _WindowsPath_


class RPath(Path) :
    """More construction methods and some other utility methods"""
    def __new__(cls, *args, **kvps):
        return super().__new__(WindowsPath if os.name == 'nt' else PosixPath, *args, **kvps)

    @classmethod
    def texnew(cls):
        return cls.home() / '.texnew'

    @classmethod
    def workspace(cls):
        return cls.home() / '.texnew' / '.workspace'

    @classmethod
    def templates(cls):
        return cls.home() / '.texnew' / 'templates'

    def read_yaml(self):
        return yaml.safe_load(self.read_text())

    def safe_rename(self):
        """Safely rename a file pointed to by path"""
        for t in itertools.count():
            new_path = self.with_name("{}_{}".format(self.stem, t) + "".join(self.suffixes))
            if not new_path.exists():
                self.rename(new_path)
                break

    @staticmethod
    def clean_workspace():
        """Deletes all files in '~/.texnew/.workspace' except .gitignore"""
        for p in RPath.workspace().iterdir():
            if not p.name == ".gitignore":
                p.unlink()


class WindowsPath(_WindowsPath_, RPath) :
    pass


class PosixPath(_PosixPath_, RPath) :
    pass
