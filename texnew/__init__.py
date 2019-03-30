"""
TexNew

Automatic LaTeX template management.

:copyright: (c) 2019 by Alex Rutar
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.4"

from texnew.test import parse_errors, test
from texnew.template import build, update
from texnew.document import Document, Divider, TexnewDocument
