from .__version__ import __version__

from .ndrepr import NDRepr, aNDRepr
from .manager import assertion, AssertionManager
from .dataclass import AbstractDataClass
from .functions import load_readme

__doc__ = load_readme()
del load_readme

__author__ = "B. F. van Beek"
__email__ = 'b.f.van.beek@vu.nl'
__version__ = __version__

__all__ = [
    'assertion', 'AssertionManager',
    'NDRepr', 'aNDRepr',
    'AbstractDataClass'
]
