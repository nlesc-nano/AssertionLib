"""
assertionlib.functions
======================

Various functions related to the `AssertionManager()` class.

Index
-----
.. currentmodule:: assertionlib.functions
.. autosummary::
    get_sphinx_domain
    wrap_docstring
    bind_callable
    allclose
    len_eq

API
---
.. autofunction:: get_sphinx_domain
.. autofunction:: wrap_docstring
.. autofunction:: bind_callable
.. autofunction:: allclose
.. autofunction:: len_eq

"""

import os
import types
import inspect
from typing import Callable, Any, Optional, Union, Sized, Dict, Mapping


def bind_callable(class_type: Union[type, Any], func: Callable,
                  name: Optional[str] = None) -> None:
    """Take a callable and use it to create a new assertion method for **class_type**.

    Examples
    --------
    Supplying the :func:`len` will create (and bind) a callable which
    performs :code:`assert len(*args, **kwargs)`

    Parameters
    ----------
    class_type : :class:`type` or :data:`Any<typing.Any>`
        A class (*i.e.* a :class:`type` instance) or class instance.

    func : :data:`Callable<typing.Callable>`
        A callable object whose output will be asserted by the created method.

    name : :class:`str`, optional
        The name of the name of the new method.
        If ``None``, use the name of **func**.


    :rtype: :data:`None`

    """
    func_name = name if name is not None else func.__name__

    # Create the to-be added method
    def method(self, *args, invert=False, **kwargs):
        self.assert_(func, *args, invert=invert, **kwargs)

    # Update docstrings and annotations
    method.__doc__ = wrap_docstring(func)
    method.__annotations__ = {'args': Any, 'kwargs': Any, 'invert': bool, 'return': None}

    # Set the new method
    if isinstance(class_type, type):  # A class
        setattr(class_type, func_name, method)
    else:  # A class instance
        _method = types.MethodType(method, class_type)
        setattr(class_type, func_name, _method)


def wrap_docstring(func: Callable) -> str:
    """Create a new NumPy style assertion docstring from the docstring of **func**.

    The summary of **funcs'** docstring, if available, is added to the ``"See also"`` section,
    in addition with an intersphinx-compatible link to **func**.

    Examples
    --------
    .. code:: python

        >>> docstring: str = wrap_docstring(isinstance)
        >>> print(docstring)
        Perform the following assertion: :code:`assert isinstance(*args, **kwargs)`.

            See also
            --------
            :func:`isinstance<isinstance>`:
                Return whether an object is an instance of a class or of a subclass thereof.

    Parameters
    ----------
    func : :data:`Callable<typing.Callable>`
        A callable whose output is to-be asserted.

    Returns
    -------
    :class:`str`
        A new docstring constructed from **funcs'** docstring.

    """
    domain = get_sphinx_domain(func)

    # Extract the first line from the func docstring
    try:
        func_summary = func.__doc__.split('\n', 1)[0]
    except AttributeError:
        func_summary = 'No description.'

    # Return a new docstring
    name = func.__qualname__ if hasattr(func, '__qualname__') else func.__name__
    return ('Perform the following assertion: '
            f':code:`assert {name}(*args, **kwargs)`.\n\n    See also\n    --------\n'
            f'    {domain}:\n'
            f'        {func_summary}\n\n    ')


#: A dictionary which translates certain __module__ values to actual valid modules
MODULE_DICT: Dict[str, str] = {
    'builtins': '',
    'genericpath': 'os.path.',
    'posixpath': 'os.path.',
    '_operator': 'operator.'
}


def _is_builtin_func(func) -> bool: return inspect.isbuiltin(func) and '.' not in func.__qualname__


def get_sphinx_domain(func: Callable, module_mapping: Mapping[str, str] = MODULE_DICT) -> str:
    """Create a Sphinx domain for **func**.

    Examples
    --------
    .. code:: python

        >>> from collections import OrderedDict

        >>> value1: str = get_sphinx_domain(int)
        >>> print(value1)
        :class:`int<int>`

        >>> value2: str = get_sphinx_domain(list.count)
        >>> print(value2)
        :meth:`list.count<list.count>`

        >>> value3: str = get_sphinx_domain(OrderedDict)
        >>> print(value3)
        :class:`OrderedDict<collections.OrderedDict>`

        >>> value4: str = get_sphinx_domain(OrderedDict.keys)
        >>> print(value4)
        :meth:`OrderedDict.keys<collections.OrderedDict.keys>`

    Parameters
    ----------
    func : :data:`Callable<typing.Callable>`
        A class or (builtin) method or function.

    module_mapping : :class:`dict` [:class:`str`, :class:`str`]
        A dictionary for mapping :attr:`__module__` values to actual module names.
        Useful for whenever there is a discrepancy between the two,
        *e.g.* the `genericpath` module of :func:`os.path.join`.

    Returns
    -------
    :class:`str`
        A string with a valid Sphinx refering to **func**.

    Raises
    ------
    TypeError
        Raised if **func** is neither a class or a (builtin) function or method.

    """
    name = func.__qualname__ if hasattr(func, '__qualname__') else func.__name__

    try:
        _module = func.__module__
    except AttributeError:  # Unbound methods don't have the `__module__` attribute
        _module = func.__objclass__.__module__

    try:
        module = MODULE_DICT[_module]
    except KeyError:
        module = _module + '.' if _module is not None else ''

    if inspect.isbuiltin(func) or inspect.isfunction(func) or _is_builtin_func(func):
        return f':func:`{name}<{module}{name}>`'
    elif inspect.ismethod(func) or inspect.ismethoddescriptor(func) or inspect.isbuiltin(func):
        return f':meth:`{name}<{module}{name}>`'
    elif inspect.isclass(func):
        return f':class:`{name}<{module}{name}>`'
    raise TypeError(f"{repr(name)} is neither a (builtin) function, method nor class")


def load_readme(readme: str = 'README.rst',
                replace: Mapping[str, str] = {'``': '|', '()': ''},
                **kwargs: Any) -> str:
    r"""Load and return the content of a readme file located in the same directory as this file.

    Equivalent to importing the content of ``../README.rst``.

    Parameters
    ----------
    readme : :class:`str`
        The name of the readme file.

    replace : :class:`dict` [:class:`str`, :class:`str`]
        A mapping of to-be replaced substrings contained within the readme file.

    \**kwargs : :data:`Any<typing.Any>`
        Optional keyword arguments for the :meth:`read<io.TextIOBase.read>` method.

    Returns
    -------
    :class:`str`
        The content of ``../README.rst``.

    """
    readme: str = os.path.join(os.path.dirname(__file__), readme)
    with open(readme, 'r') as f:
        ret = f.read(**kwargs)
    for old, new in replace.items():
        ret = ret.replace(old, new)
    return ret


def len_eq(a: Sized, b: int) -> bool:
    """Check if the length of **a** is equivalent to **b**."""
    return len(a) == b


def allclose(a: float, b: float, rtol: float = 1e-07) -> bool:
    """Check if the absolute differnce between **a** and **b** is smaller than **rtol**."""
    delta = abs(a - b)
    return delta < rtol


yup = load_readme()
