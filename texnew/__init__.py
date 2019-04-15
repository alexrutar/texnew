"""
TexNew

Automatic LaTeX template management.

:copyright: (c) 2019 by Alex Rutar
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.8"

from .template import build, update
from .document import Document, Divider, TexnewDocument
from .rpath import RPath
