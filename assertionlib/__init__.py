"""AssertionLib."""

import os
from nanoutils import VersionInfo

from .__version__ import __version__

from .ndrepr import NDRepr, aNDRepr
from .manager import assertion, AssertionManager
from .dataclass import AbstractDataClass
from .functions import load_readme

_README = os.path.join(__path__[0], 'README.rst')  # type: ignore
__doc__ = load_readme(_README, encoding='utf-8')
version_info = VersionInfo.from_str(__version__)

del _README, load_readme, os, VersionInfo

__author__ = "B. F. van Beek"
__email__ = 'b.f.van.beek@vu.nl'


__all__ = [
    'assertion', 'AssertionManager',
    'NDRepr', 'aNDRepr',
    'AbstractDataClass'
]
