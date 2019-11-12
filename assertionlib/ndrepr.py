"""
assertionlib.ndrepr
====================

A module for holding the :class:`NDRepr` class, a subclass of the builtin :class:`reprlib.Repr` class.

Index
-----
.. currentmodule:: assertionlib.ndrepr
.. autosummary::
    NDRepr

Type-specific repr methods:

.. autosummary::
    :nosignatures:

    NDRepr.repr_float
    NDRepr.repr_Exception
    NDRepr.repr_Signature
    NDRepr.repr_method
    NDRepr.repr_method_descriptor
    NDRepr.repr_function
    NDRepr.repr_builtin_function_or_method
    NDRepr.repr_type
    NDRepr.repr_module
    NDRepr.repr_Molecule
    NDRepr.repr_Settings
    NDRepr.repr_Atom
    NDRepr.repr_Bond
    NDRepr.repr_ndarray
    NDRepr.repr_DataFrame
    NDRepr.repr_Series

API
---
.. autoclass:: NDRepr
.. automethod:: NDRepr.repr_float
.. automethod:: NDRepr.repr_Exception
.. automethod:: NDRepr.repr_Signature
.. automethod:: NDRepr.repr_method
.. automethod:: NDRepr.repr_method_descriptor
.. automethod:: NDRepr.repr_function
.. automethod:: NDRepr.repr_builtin_function_or_method
.. automethod:: NDRepr.repr_type
.. automethod:: NDRepr.repr_module
.. automethod:: NDRepr.repr_Molecule
.. automethod:: NDRepr.repr_Settings
.. automethod:: NDRepr.repr_Atom
.. automethod:: NDRepr.repr_Bond
.. automethod:: NDRepr.repr_ndarray
.. automethod:: NDRepr.repr_DataFrame
.. automethod:: NDRepr.repr_Series

"""  # noqa

import types
import inspect
import reprlib
import builtins
import textwrap
from typing import Any, Dict, Callable, Union, Tuple
from itertools import chain, islice

try:
    from scm.plams import Molecule, Atom, Bond, Settings
except ImportError:
    Molecule = 'scm.plams.mol.molecule.Molecule'
    Atom = 'scm.plams.mol.molecule.Atom'
    Bond = 'scm.plams.mol.molecule.Bond'
    Settings = 'scm.plams.core.settings.Settings'

try:
    import numpy as np
    ndarray = np.ndarray
except ImportError:
    ndarray = 'numpy.ndarray'

try:
    import pandas as pd
    DataFrame, Series = pd.DataFrame, pd.Series
except ImportError:
    DataFrame, Series = 'pandas.DataFrame', 'pandas.Series'

__all__ = ['NDRepr', 'aNDRepr']

BuiltinType = Union[types.BuiltinFunctionType, types.BuiltinMethodType]


class NDRepr(reprlib.Repr):
    """A subclass of :class:`reprlib.Repr` with methods for handling additional object types.

    Has additional methods for handling:

        * PLAMS Molecules, Atoms, Bonds and Settings
        * NumPy arrays
        * Pandas Series and DataFrames
        * Callables

    Examples
    --------
    See :mod:`reprlib` for more details.

    code:: python

        >>> from assertionlib.ndrepr import aNDRepr
        >>> import numpy as np

        >>> object = np.ones((100, 100), dtype=float)
        >>> print(aNDRepr.repr(object))
        array([[1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],
               [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],
               [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],
               ...,
               [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],
               [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],
               [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000]])

    Parameters
    ----------
    **kwargs : object
        User-specified values for one or more :class:`NDRepr` instance attributes.
        An :exc:`AttributeError` is raised upon encountering unrecognized keys.

    Attributes
    ----------
    maxSignature : :class:`int`
        The maximum length of callables' signatures before further parameters are truncated.
        See also :meth:`NDRepr.repr_Signature`.

    maxfloat : :class:`int`
        The number of to-be displayed :class:`float` decimals.
        See also :meth:`NDRepr.repr_float`.

    maxMolecule : :class:`int`
        The maximum number of to-be displayed atoms and bonds in PLAMS molecules.
        See also :meth:`NDRepr.repr_Molecule`.

    maxndarray : :class:`int`
        The maximum number of items in a :class:`numpy.ndarray` row.
        Passed as argument to the :func:`numpy.printoptions` function:

        * :code:`threshold = self.maxndarray`
        * :code:`edgeitems = self.maxndarray // 2`

        See also :meth:`NDRepr.repr_ndarray`.

    maxSeries : :class:`int`
        The maximum number of rows per :class:`pandas.Series` instance.
        Passed as value to :attr:`pandas.options.display`.

        * :code:`pandas.options.display.max_rows = self.series`

        See also :meth:`NDRepr.repr_Series`.

    maxDataFrame : :class:`int`
        The maximum number of rows per :class:`pandas.DataFrame` instance.
        Passed as values to :attr:`pandas.options.display`:

        * :code:`pandas.options.display.max_rows = self.maxdataframe`
        * :code:`pandas.options.display.max_columns = self.maxdataframe // 2`

        See also :meth:`NDRepr.repr_DataFrame`.

    np_printoptions : :class:`dict`
        Additional keyword arguments for :func:`numpy.printoptions`.

        .. note::
            Arguments provided herein will take priority over those specified internally
            in :meth:`NDRepr.repr_ndarray`.

    pd_printoptions : :class:`dict`
        Additional "keyword arguments" for :attr:`pandas.options`.

        .. note::
            Arguments provided herein will take priority over those specified internally
            in :meth:`NDRepr.repr_DataFrame` and :meth:`NDRepr.repr_Series`.

    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a :class:`NDRepr` instance."""
        super().__init__()
        self.maxstring: int = 80

        # New instance attributes
        self.maxSignature: int = self.maxstring - 20
        self.maxException: int = 1000
        self.maxfloat: int = 4
        self.maxndarray: int = 6
        self.maxSeries: int = 12
        self.maxDataFrame: int = 12
        self.maxMolecule: int = 6
        self.maxSettings: int = self.maxdict
        self.np_printoptions: Dict[str, Any] = {}
        self.pd_printoptions: Dict[str, Any] = {}

        # Update attributes based on **kwargs; raise an error if a key is unrecognized
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise AttributeError(f'{repr(self.__class__.__name__)} instance '
                                     f'has no attribute {repr(k)}')
            setattr(self, k, v)

    def repr1(self, obj: Any, level: int):
        if isinstance(obj, Exception):  # Refer all exceptions NDRepr.repr_Exception()
            return self.repr_Exception(obj, level)
        return super().repr1(obj, level)
    repr1.__doc__ = reprlib.Repr.repr1.__doc__

    def repr_float(self, obj: float, level: int) -> str:
        """Create a :class:`str` representation of a :class:`float` instance."""  # noqa
        i = self.maxfloat
        if 10**i < obj or obj < 10**-i:
            return f'{obj:{i}.{i}e}'
        return f'{obj:{i}.{i}f}'  # Exponential notation

    def repr_Exception(self, obj: Exception, level: int) -> str:
        """Create a :class:`str` representation of an :exc`Exception` instance."""
        value = str(obj)
        i = self.maxException
        if len(value) > i:
            value = value[:i] + '...'
        return f'{obj.__class__.__name__}({value})'

    # New methods for parsing callables

    def repr_method(self, obj: types.MethodType, level: int) -> str:
        """Create a :class:`str` representation of a bound method."""
        name, signature = self._parse_callable(obj, level)
        return f"<bound method '{name}{signature}'>"

    def repr_method_descriptor(self, obj: 'types.MethodDescriptorType', level: int) -> str:
        """Create a :class:`str` representation of an unbound method."""
        name, signature = self._parse_callable(obj, level)
        return f"<method '{name}{signature}'>"

    def repr_function(self, obj: types.FunctionType, level: int) -> str:
        """Create a :class:`str` representation of a function."""
        name, signature = self._parse_callable(obj, level)
        return f"<function '{name}{signature}'>"

    def repr_builtin_function_or_method(self, obj: BuiltinType, level: int) -> str:
        """Create a :class:`str` representation of a builtin function or method."""
        name, signature = self._parse_callable(obj, level)
        if '.' in obj.__qualname__:
            return f"<built-in bound method '{name}{signature}'>"
        return f"<built-in function '{name}{signature}'>"

    def repr_type(self, obj: type, level: int) -> str:
        """Create a :class:`str` representation of a :class:`type` object."""
        name, signature = self._parse_callable(obj, level)
        return f"<class '{name}{signature}'>"

    def repr_module(self, obj: types.ModuleType, level: int) -> str:
        """Create a :class:`str` representation of a module."""
        return f"<module '{obj.__name__}'>"

    def repr_Signature(self, obj: inspect.Signature, level: int) -> str:
        """Create a :class:`str` representation of a :class:`inspect.Signature` instance."""
        i = self.maxSignature
        signature = str(obj)

        # Return the signature without parameter truncation
        if len(signature) <= i:
            return signature

        # Truncate the number of to-be displayed parameters based the 'level' parameter
        param, ret = signature.rsplit(')', 1)
        if level <= 0:
            return f'(...){ret}'

        # Truncate the number of to-be displayed parameters based on self.maxSignature
        iterator = iter(param.split(', '))
        param_accumulate = next(iterator)
        for param in iterator:
            signature = f'{param_accumulate}, {param}){ret}'
            if len(signature) > i:
                param_accumulate += ', ...'
                break
            param_accumulate += f', {param}'

        return f'{param_accumulate}){ret}'

    def _parse_callable(self, obj: Callable, level: int) -> Tuple[str, str]:
        """Create a :class:`str` representation of the name and signature of a callable."""
        # Construct the name of the callable
        try:
            name = obj.__qualname__
        except AttributeError:
            name = obj.__name__

        # Construct the signature
        try:
            _signature = inspect.signature(obj)
            signature = self.repr1(_signature, level - 1)
        except ValueError:
            signature = '(...)'

        return name, signature

    # New PLAMS-related methods

    def repr_Molecule(self, obj: Molecule, level: int) -> str:
        """Create a :class:`str` representation of a |plams.Molecule| instance."""
        if level <= 0:
            return f'{obj.__class__.__name__}(...)'
        elif not obj:
            return f'{obj.__class__.__name__}()'

        obj.set_atoms_id()
        ret = 'Atoms: \n'
        i = self.maxMolecule

        # Print atoms
        kwargs = {'decimal': self.maxfloat, 'space': 14 - (6 - self.maxfloat)}
        for atom in obj.atoms[:i]:
            ret += f'  {atom.id:<5d}{atom.str(**kwargs).strip()}\n'
        if len(obj.atoms) > i:
            ret += '  ...\n'

        # Print bonds
        if len(obj.bonds):
            ret += 'Bonds: \n'
            for bond in obj.bonds[:i]:
                ret += f'  ({bond.atom1.id})--{bond.order:1.1f}--({bond.atom2.id})\n'
            if len(obj.bonds) > i:
                ret += '  ...\n'

        # Print lattice vectors
        if obj.lattice:
            ret += 'Lattice:\n'
            for vec in obj.lattice:
                ret += '  {:16.10f} {:16.10f} {:16.10f}\n'.format(*vec)

        obj.unset_atoms_id()
        indent = 4 * ' '
        return f'{obj.__class__.__name__}(\n{textwrap.indent(ret[:-1], indent)}\n)'

    def repr_Settings(self, obj: Settings, level: int) -> str:
        """Create a :class:`str` representation of a |plams.Settings| instance."""
        n = len(obj)
        if not obj:
            return f'{obj.__class__.__name__}()'
        elif level <= 0:
            return '\n...'

        pieces = []
        indent = 4 * ' '
        newlevel = level - 1

        for k, v in islice(obj.items(), self.maxSettings):
            key = str(k)
            value = self.repr1(v, newlevel)
            pieces.append(f'\n{key}:')
            if type(obj) is type(value):
                pieces.append(f'{textwrap.indent(value, indent)}:')
            else:
                pieces.append(f'{textwrap.indent(value, indent)}')

        if n > self.maxSettings:
            pieces.append('\n...')

        ret = ''.join(pieces)
        if level == self.maxlevel:
            return f'{obj.__class__.__name__}(\n{textwrap.indent(ret[1:], indent)}\n)'
        return ret

    def repr_Atom(self, obj: Atom, level: int) -> str:
        """Create a :class:`str` representation of a |plams.Atom| instance."""
        decimal = self.maxfloat
        space = 14 - (6 - decimal)  # The default PLAMS values for space and decimal are 14 and 6
        ret = obj.str(decimal=decimal, space=space).strip()
        return f'{obj.__class__.__name__}({ret})'

    def repr_Bond(self, obj: Bond, level: int) -> str:
        """Create a :class:`str` representation of a |plams.Bond| instance."""
        return f'{obj.__class__.__name__}({obj})'

    # NumPy- and Pandas-related methods

    def repr_ndarray(self, obj: ndarray, level: int) -> str:
        """Create a :class:`str` representation of a :class:`numpy.ndarray` instance."""
        if level <= 0:
            return f'{obj.__class__.__name__}(...)'

        kwargs = {'threshold': self.maxndarray,
                  'edgeitems': self.maxndarray // 2,
                  'formatter': self._get_ndformatter(obj)}
        kwargs.update(self.np_printoptions)

        with np.printoptions(**kwargs):
            return builtins.repr(obj)

    def repr_DataFrame(self, obj: DataFrame, level: int) -> str:
        """Create a :class:`str` representation of a :class:`pandas.DataFrame` instance."""
        if level <= 0:
            return f'{obj.__class__.__name__}(...)'

        kwargs = {'display.max_rows': self.maxDataFrame,
                  'display.max_columns': self.maxDataFrame // 2}
        kwargs.update(self.pd_printoptions)
        args = chain.from_iterable(kwargs.items())

        with pd.option_context(*args):
            return builtins.repr(obj)

    def repr_Series(self, obj: Series, level: int) -> str:
        """Create a :class:`str` representation of a :class:`pandas.Series` instance."""
        if level <= 0:
            return f'{obj.__class__.__name__}(...)'

        kwargs = {'display.max_rows': self.maxSeries}
        kwargs.update(self.pd_printoptions)
        args = chain.from_iterable(kwargs.items())

        with pd.option_context(*args):
            return builtins.repr(obj)

    def _get_ndformatter(self, obj: ndarray) -> dict:
        """Return a value for the **formatter** argument in :func:`numpy.printoptions`."""
        if obj.dtype not in (np.dtype(float), np.dtype(int)):
            return {}

        try:
            max_len = len(str(int(obj.max())))
            min_len = len(str(int(obj.min())))
        except ValueError:  # Raised when encountering zero-sized arrays
            width = 0
        else:
            width = max(max_len, min_len)

        if obj.dtype == np.dtype(float):
            width += 5
            value = '{' + f':{width}.{self.maxfloat}f' + '}'
            return {'float': value.format}
        else:  # obj.dtype == np.dtype(int)
            value = '{' + f':{width}d' + '}'
            return {'int': value.format}


#: An instance of :class:`NDRepr`.
aNDRepr: NDRepr = NDRepr()
