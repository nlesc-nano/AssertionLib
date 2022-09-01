"""AssertionLib."""

import os
import sys
from nanoutils import VersionInfo

from .__version__ import __version__ as __version__
if sys.version_info >= (3, 7):
    version_info = VersionInfo.from_str(__version__)
else:
    version_info = VersionInfo._make(int(i) for i in __version__.split(".") if i.isnumeric())

from .ndrepr import NDRepr, aNDRepr
from .manager import assertion, AssertionManager
from .dataclass import AbstractDataClass
from .functions import load_readme

_README = os.path.join(__path__[0], 'README.rst')  # type: ignore
__doc__ = load_readme(_README, encoding='utf-8')

del _README, load_readme, os, sys, VersionInfo

__author__ = "B. F. van Beek"
__email__ = 'b.f.van.beek@vu.nl'


__all__ = [
    'assertion', 'AssertionManager',
    'NDRepr', 'aNDRepr',
    'AbstractDataClass'
]
