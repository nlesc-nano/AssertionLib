from .__version__ import __version__

from .manager import assertion, AssertionManager
from .functions import load_readme

__doc__ = load_readme()
__version__ = __version__
__author__ = "B. F. van Beek"
__email__ = 'b.f.van.beek@vu.nl'

__all__ = ['assertion', 'AssertionManager']
