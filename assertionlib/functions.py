"""
assertionlib.functions
======================

Various functions related to the :class:`.AssertionManager` class.

Index
-----
.. currentmodule:: assertionlib.functions
.. autosummary::
    get_sphinx_domain
    create_assertion_doc
    bind_callable
    skip_if
    to_positional

API
---
.. autofunction:: get_sphinx_domain
.. autofunction:: create_assertion_doc
.. autofunction:: bind_callable
.. autofunction:: skip_if
.. autofunction:: to_positional

"""

import os
import sys
import textwrap
import warnings
import functools
from types import MappingProxyType, MethodType
from typing import (
    Callable,
    Any,
    Optional,
    Union,
    Mapping,
    Type,
    TypeVar,
    Iterable,
    List,
    Tuple,
    cast,
    TYPE_CHECKING
)
from inspect import (
    signature,
    Parameter,
    Signature,
    isbuiltin,
    isfunction,
    ismethod,
    ismethoddescriptor,
    isclass
)

if sys.version_info <= (3, 6):
    COMMA = ','
else:
    COMMA = ''

if TYPE_CHECKING:
    from enum import IntEnum
else:
    IntEnum = 'enum.IntEnum'

__all__ = [
    'set_docstring', 'get_sphinx_domain', 'create_assertion_doc', 'bind_callable', 'skip_if'
]

T = TypeVar('T')

PO = Parameter.POSITIONAL_ONLY
POK = Parameter.POSITIONAL_OR_KEYWORD
VP = Parameter.VAR_POSITIONAL
KO = Parameter.KEYWORD_ONLY
VK = Parameter.VAR_KEYWORD
_empty = Parameter.empty

PARAM_NAME_MAPPING: Mapping[IntEnum, str] = MappingProxyType({
    PO: 'positional-only',
    POK: 'positional or keyword',
    VP: 'variadic positional',
    KO: 'keyword-only',
    VK: 'variadic keyword'
})

DEFAULT_PRM: Tuple[Parameter, Parameter] = (
    Parameter('args', Parameter.VAR_POSITIONAL, annotation=Any),
    Parameter('kwargs', Parameter.VAR_KEYWORD, annotation=Any)
)


def _to_positional(iterable: Iterable[Parameter]) -> List[Parameter]:
    """Helper function for :func:`to_positional`; used in creating the new :class:`~inspect.Parameter` list."""  # noqa
    ret = []
    for prm in iterable:
        if prm.kind is not POK:
            ret.append(prm)
        elif prm.default is _empty:
            ret.append(prm.replace(kind=PO))
        else:
            ret.append(prm.replace(kind=KO))
    return ret


def to_positional(func: Callable[..., T]) -> Callable[..., T]:
    r"""Decorate a function's :attr:`__signature__` such that all positional-or-keyword arguments are changed to either positional- or keyword-only.

    Example
    -------
    .. code:: python

        >>> from inspect import signature
        >>> from assertionlib.functions import to_positional

        >>> def func1(a: int, b: int = 0) -> int:
        ...     pass

        >>> @to_positional
        ... def func2(a: int, b: int = 0) -> int:
        ...     pass

        >>> print(signature(func1), signature(func2), sep='\n')
        (a: int, b: int = 0) -> int
        (a: int, /, *, b: int = 0) -> int

    """  # noqa
    sgn = signature(func)
    prm_dict = sgn.parameters

    prm_list = _to_positional(prm_dict.values())
    func.__signature__ = Signature(  # type: ignore
        parameters=prm_list, return_annotation=sgn.return_annotation
    )
    return func


def set_docstring(docstring: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """A decorator for assigning docstrings."""
    def wrapper(func: Callable[..., T]) -> Callable[..., T]:
        func.__doc__ = docstring
        return func
    return wrapper


def bind_callable(class_type: Union[type, Any], func: Callable,
                  name: Optional[str] = None, warn: bool = True) -> None:
    """Take a callable and use it to create a new assertion method for **class_type**.

    The created callable will have the same signature as **func** except for one additional
    keyword argument by the name of ``func`` (default value: :data:`False`).
    Setting this keyword argument to :data:`True` will invert the output of the assertion,
    *i.e.* it changes ``assert func(...)`` into ``assert not func(...)``.

    Examples
    --------
    Supplying the builtin :func:`len` function will create (and bind) a callable which
    performs the :code:`assert len(obj)` assertion.

    Parameters
    ----------
    class_type : :class:`type` or :data:`~typing.Any`
        A class (*i.e.* a :class:`type` instance) or class instance.

    func : :class:`~collections.abc.Callable`
        A callable object whose output will be asserted by the created method.

    name : :class:`str`, optional
        The name of the name of the new method.
        If ``None``, use the name of **func**.


    :rtype: :data:`None`

    """
    # Create the new function
    function = create_assertion_func(func)
    if name is not None:
        function.__name__ = name

    # Set the new method
    if isinstance(class_type, type):  # A class
        function.__qualname__ = f'{class_type.__name__}.{function.__name__}'
        function.__module__ = class_type.__module__
        setattr(class_type, function.__name__, function)

    else:  # A class instance
        function.__qualname__ = f'{class_type.__class__.__name__}.{function.__name__}'
        function.__module__ = class_type.__class__.__module__
        method = MethodType(function, class_type)  # Create a bound method
        setattr(class_type, function.__name__, method)


def create_assertion_func(func: Callable[..., Any]) -> Callable[..., None]:
    __tracebackhide__ = True

    def wrapper(self, *args: Any,
                invert: bool = False,
                exception: Optional[Type[Exception]] = None,
                post_process: Optional[Callable[[Any], Any]] = None,
                message: Optional[str] = None,
                **kwargs: Any) -> None:
        __tracebackhide__ = True

        self.assert_(
            func, *args,
            exception=exception, invert=invert, post_process=post_process, message=message,
            **kwargs
        )

    # Create a new list of Parameter instances
    # All keyword-or-positional parameters are converted into positional- or keyword-only
    try:
        _prm_values = signature(func).parameters.values()
        prm_list = _to_positional(_prm_values)
    except ValueError:
        prm_list = list(DEFAULT_PRM)
    else:
        if prm_list[-1].kind is not VK:
            prm_list.append(Parameter('kwargs', kind=VK, annotation=Any))
    finally:
        prm_list.insert(0, Parameter('self', kind=PO))

    wrapper.__name__ = wrapper.__qualname__ = func.__name__
    wrapper.__doc__ = create_assertion_doc(func)
    wrapper.__signature__ = Signature(parameters=prm_list, return_annotation=None)  # type: ignore
    return wrapper


#: A string with the (to-be formatted) docstring returned by :func:`wrap_docstring`
BASE_DOCSTRING: str = r"""Perform the following assertion: :code:`assert {name}{signature}`.

Parameters
----------
{parameters}

Keyword Arguments
-----------------
invert : :class:`bool`
    If :data:`True`, invert the output of the assertion:
    :code:`assert not {name}{signature}`.

exception : :class:`type` [:exc:`Exception`], optional
    Assert that **exception** is raised during/before the assertion operation.

post_process : :data:`Callable[[Any], bool]<typing.Callable>`, optional
    Apply post-processing to the to-be asserted data before asserting aforementioned data.
    Example values would be the likes of :func:`any()<python:any>` and :func:`all()<python:all>`.

message : :class:`str`, optional
    A custom error message to-be passed to the ``assert`` statement.


:rtype: :data:`None`

See also
--------
{domain}:
{summary}
"""


def create_assertion_doc(func: Callable) -> str:
    r"""Create a new NumPy style assertion docstring from the docstring of **func**.

    The summary of **funcs'** docstring, if available, is added to the ``"See also"`` section,
    in addition with an intersphinx-compatible link to **func**.

    Examples
    --------
    .. code:: python

        >>> from assertionlib.functions import create_assertion_doc

        >>> docstring: str = create_assertion_doc(isinstance)
        >>> print(docstring)
        Perform the following assertion: :code:`assert isinstance(*args, **kwargs)`.
        <BLANKLINE>
        Parameters
        ----------
        invert : :class:`bool`
            Invert the output of the assertion: :code:`assert not isinstance(*args, **kwargs)`.
            This value should only be supplied as keyword argument.
        <BLANKLINE>
        exception : :class:`type` [:exc:`Exception`], optional
            Assert that **exception** is raised during/before the assertion operation.
            This value should only be supplied as keyword argument.
        <BLANKLINE>
        post_process : :class:`~collections.abc.Callable`, optional
            Apply post-processing to the to-be asserted data before asserting aforementioned data.
            Example functions would be the likes of :func:`~builtins.any` and :func:`~builtins.all`.
        <BLANKLINE>
        message : :class:`str`, optional
            A custom error message to-be passed to the ``assert`` statement.
        <BLANKLINE>
        \*args/\**kwargs : :data:`~typing.Any`
            Parameters for catching excess variable positional and keyword arguments.
        <BLANKLINE>
        <BLANKLINE>
        :rtype: :data:`None`
        <BLANKLINE>
        See also
        --------
        :func:`isinstance()<python:isinstance>`:
            Return whether an object is an instance of a class or of a subclass thereof.
        <BLANKLINE>
            A tuple, as in ``isinstance(x, (A, B, ...))``, may be given as the target to
            check against. This is equivalent to ``isinstance(x, A) or isinstance(x, B)
            or ...`` etc.
        <BLANKLINE>

    Parameters
    ----------
    func : :class:`~collections.abc.Callable`
        A callable whose output is to-be asserted.

    Returns
    -------
    :class:`str`
        A new docstring constructed from **funcs'** docstring.

    """
    try:
        __sgn = signature(func)
        sgn = Signature(_to_positional(__sgn.parameters.values()), return_annotation=None)
    except ValueError:
        sgn = Signature(parameters=DEFAULT_PRM, return_annotation=None)
        sgn_str = '(*args, **kwargs)'
    else:
        sgn_str = '(' + ', '.join((k if v.default is _empty else f'{k}={k}') for k, v in sgn.parameters.items()) + ')'

    name = getattr(func, '__qualname__', func.__name__)
    domain = get_sphinx_domain(func)
    summary = textwrap.indent(func.__doc__ or 'No description.', 4 * ' ')

    parameters = ''
    for k, v in sgn.parameters.items():
        prm_type = PARAM_NAME_MAPPING[v.kind]
        parameters += f'{k}\n    The {prm_type} argument ``{k}``  of {domain}.\n\n'

    return BASE_DOCSTRING.format(
        parameters=parameters, name=name, signature=sgn_str, domain=domain, summary=summary
    )


#: A dictionary which translates certain __module__ values to an actual valid modules
MODULE_DICT: Mapping[str, str] = MappingProxyType({
    'genericpath': 'os.path',
    'posixpath': 'os.path',
    '_operator': 'operator'
})


def _is_builtin_func(func: Callable) -> bool:
    """Check if **func** is a builtin function."""
    try:
        return isbuiltin(func) and '.' not in getattr(func, '__qualname__', '')
    except AttributeError:
        return False


def get_sphinx_domain(func: Callable, module_mapping: Mapping[str, str] = MODULE_DICT) -> str:
    """Create a Sphinx domain for **func**.

    Examples
    --------
    .. code:: python

        >>> from collections import OrderedDict
        >>> from assertionlib.functions import get_sphinx_domain

        >>> value1: str = get_sphinx_domain(int)
        >>> print(value1)
        :class:`int<python:int>`

        >>> value2: str = get_sphinx_domain(list.count)
        >>> print(value2)
        :meth:`list.count()<python:list.count>`

        >>> value3: str = get_sphinx_domain(OrderedDict)
        >>> print(value3)
        :class:`~collections.OrderedDict`

        >>> value4: str = get_sphinx_domain(OrderedDict.keys)
        >>> print(value4)
        :meth:`~collections.OrderedDict.keys`

    Parameters
    ----------
    func : :class:`~collections.abc.Callable`
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
    name: str = getattr(func, '__qualname__', func.__name__)

    # Extract the __module__ from **func**
    try:
        _module = func.__module__
    except AttributeError:  # Unbound methods don't have the `__module__` attribute
        _module = func.__objclass__.__module__  # type: ignore

    # Convert the extracted __module__ into an actual valid module
    module = MODULE_DICT.get(_module, _module)

    # Identify the sphinx domain
    if isfunction(func) or _is_builtin_func(func):
        directive = 'func'
    elif ismethod(func) or ismethoddescriptor(func) or isbuiltin(func):
        directive = 'meth'
    elif isclass(func):
        directive = 'class'

    # Return the domain as either :func:`...`, :meth:`...` or :class:`...`
    try:
        if module != 'builtins':
            return f':{directive}:`~{module}.{name}`'
        else:
            parenthesis = '()' if directive in {'func', 'meth'} else ''
            return f':{directive}:`{name}{parenthesis}<python:{name}>`'
    except UnboundLocalError as ex:
        raise TypeError(f"{name!r} is neither a (builtin) function, method nor class") from ex


#: An immutable mapping of to-be replaced substrings and their replacements.
README_MAPPING: Mapping[str, str] = MappingProxyType({
    '``': '|',
    '()': ''
})


def load_readme(readme: Union[str, os.PathLike] = 'README.rst',
                replace: Mapping[str, str] = README_MAPPING,
                **kwargs: Any) -> str:
    r"""Load and return the content of a readme file located in the same directory as this file.

    Equivalent to importing the content of ``../README.rst``.

    Parameters
    ----------
    readme : :class:`str`
        The name of the readme file.

    replace : :class:`dict` [:class:`str`, :class:`str`]
        A mapping of to-be replaced substrings contained within the readme file.

    \**kwargs : :data:`~typing.Any`
        Optional keyword arguments for the :meth:`~io.TextIOBase.read` method.

    Returns
    -------
    :class:`str`
        The content of ``../README.rst``.

    """
    readme_abs: str = os.path.join(os.path.dirname(__file__), readme)
    with open(readme_abs, 'r') as f:
        ret: str = f.read(**kwargs)
    for old, new in replace.items():
        ret = ret.replace(old, new)
    return ret


NoneFunc = Callable[..., None]


@set_docstring(f"""A decorator which causes function calls to be ignored if :code:`bool(condition) is True`.

A :exc:`UserWarning` is issued if **condition** evaluates to :data:`True`.

Examples
--------
.. code:: python

    >>> import warnings
    >>> from assertionlib.functions import skip_if

    >>> condition = Exception("Error")

    >>> def func1() -> None:
    ...     print(True)

    >>> @skip_if(condition)
    ... def func2() -> None:
    ...     print(True)

    >>> func1()
    True

    >>> with warnings.catch_warnings():  # Convert the warning into a raised exception
    ...     warnings.simplefilter("error", UserWarning)
    ...     func2()
    Traceback (most recent call last):
      ...
    UserWarning: Exception('Error'{COMMA}) evaluated to True; skipping call to func2(...)

""")  # noqa: E501
def skip_if(condition: Any) -> Callable[[Callable[..., T]], Union[Callable[..., T], NoneFunc]]:
    """Placeholder."""
    def skip() -> None:
        return None

    def decorator(func: Callable[..., T]) -> Union[Callable[..., T], NoneFunc]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
            if not condition:
                return cast(T, func(*args, **kwargs))

            exc = UserWarning(f"{condition!r:.70} evaluated to True; skipping call to {func.__name__}(...)")  # noqa: E501
            if isinstance(condition, BaseException):
                exc.__cause__ = condition

            warnings.warn(exc, stacklevel=2)
            return cast(None, skip())
        return wrapper
    return decorator
