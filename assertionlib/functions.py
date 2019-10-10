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

API
---
.. autofunction:: get_sphinx_domain
.. autofunction:: wrap_docstring
.. autofunction:: bind_callable

"""

import types
import inspect
from typing import Callable, Any, Optional, Union, Sized


def bind_callable(class_type: Union[type, Any], func: Callable,
                  name: Optional[str] = None) -> None:
    """Take a callable and use it to create a new assertion method for **class_type**.

    Parameter
    ---------
    class_type : :class:`type` or :class:`Any<typing.Any>`
        A class (*i.e.* a :class:`type` instance) or class instance.

    func : :class:`Callable<typing.Callable>`
        A callable object whose output will be asserted by the created method.

    name : :class:`str`, optional
        The name of the name of the new method.
        If ``None``, use the name of **func**.

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
    """Create a new NumPy style assertion docstring from the docstring of **func**."""
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


def get_sphinx_domain(func: Callable) -> str:
    """Create a Sphinx domain from func.

    Accepts function, classes and methods; raises a :exc:`TypeError` otherwise.

    """
    name = func.__qualname__ if hasattr(func, '__qualname__') else func.__name__
    if inspect.isbuiltin(func) or inspect.isfunction(func):
        return f':func:`{name}<{func.__module__}.{name}>`'
    elif inspect.ismethod(func):
        return f':meth:`{name}<{func.__module__}.{name}>`'
    elif inspect.isclass(func):
        return f':class:`{name}<{func.__module__}.{name}>`'
    raise TypeError(f"{repr(name)} is neither a (builtin) function, method nor class")


def len_eq(a: Sized, b: int) -> bool:
    """Check if the length of **a** is equivalent to **b**."""
    return len(a) == b


def allclose(a: float, b: float, rtol: float = 1e-07) -> bool:
    """Check if the absolute differnce between **a** and **b** is smaller than **rtol**."""
    delta = abs(a) - abs(b)
    return delta < rtol
