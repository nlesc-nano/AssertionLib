from .__version__ import __version__

from .manager import assertion, AssertionManager
from .functions import load_readme

__doc__ = load_readme()
__author__ = "B. F. van Beek"
__email__ = 'b.f.van.beek@vu.nl'

__all__ = ['__version__', 'assertion', 'AssertionManager']
