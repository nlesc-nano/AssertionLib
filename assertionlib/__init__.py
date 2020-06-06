"""AssertionLib."""

import os
from .__version__ import __version__

from .ndrepr import NDRepr, aNDRepr
from .manager import assertion, AssertionManager
from .dataclass import AbstractDataClass
from .functions import load_readme

_README = os.path.join(__path__[0], 'README.rst')  # type: ignore
__doc__ = load_readme(_README, encoding='utf-8')

del _README, load_readme, os

__author__ = "B. F. van Beek"
__email__ = 'b.f.van.beek@vu.nl'
__version__ = __version__

__all__ = [
    'assertion', 'AssertionManager',
    'NDRepr', 'aNDRepr',
    'AbstractDataClass'
]
