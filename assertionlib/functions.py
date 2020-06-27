"""Various functions related to the :class:`.AssertionManager` class.

Index
-----
.. currentmodule:: assertionlib.functions
.. autosummary::
    get_sphinx_domain
    create_assertion_doc
    bind_callable
    to_positional

API
---
.. autofunction:: get_sphinx_domain
.. autofunction:: create_assertion_doc
.. autofunction:: bind_callable
.. autofunction:: to_positional

"""

import os
import sys
import textwrap
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

from nanoutils import set_docstring

if sys.version_info < (3, 7):
    COMMA = ','
    SPACE = ''
else:
    COMMA = ''
    SPACE = ' '

if TYPE_CHECKING:
    from enum import IntEnum
else:
    IntEnum = 'enum.IntEnum'

__all__ = [
    'get_sphinx_domain', 'create_assertion_doc', 'bind_callable', 'to_positional'
]

T = TypeVar('T')
FT = TypeVar('FT', bound=Callable[..., Any])

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
    """Helper function for :func:`to_positional`; used in creating the new :class:`~inspect.Parameter` list."""  # noqa: E501
    ret = []
    for prm in iterable:
        if prm.kind is not POK:
            ret.append(prm)
        elif prm.default is _empty:
            ret.append(prm.replace(kind=PO))
        else:
            ret.append(prm.replace(kind=KO))
    return ret


@set_docstring(f"""Decorate a function's :attr:`__signature__` such that all positional-or-keyword arguments are changed to either positional- or keyword-only.

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

    >>> print(signature(func1), signature(func2), sep='\\n')
    (a:{SPACE}int, b:{SPACE}int{SPACE}={SPACE}0) -> int
    (a:{SPACE}int, /, *, b:{SPACE}int{SPACE}={SPACE}0) -> int

""")  # noqa: E501
def to_positional(func: FT) -> FT:
    sgn = signature(func)
    prm_dict = sgn.parameters

    prm_list = _to_positional(prm_dict.values())
    func.__signature__ = Signature(  # type: ignore
        parameters=prm_list, return_annotation=sgn.return_annotation
    )
    return func


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
    """Construct an assertion function from **func**."""

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
        if not prm_list or prm_list[-1].kind is not VK:
            prm_list.append(Parameter('kwargs', kind=VK, annotation=Any))
    finally:
        if prm_list and prm_list[0].name == 'self':
            prm_list[0] = Parameter('obj', kind=PO, annotation=prm_list[0].annotation)
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
{domain}
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
        Perform the following assertion: :code:`assert isinstance(obj, class_or_tuple)`.
        <BLANKLINE>
        Parameters
        ----------
        obj
            The positional-only argument ``obj`` of :func:`isinstance()<python:isinstance>`.
        <BLANKLINE>
        class_or_tuple
            The positional-only argument ``class_or_tuple`` of :func:`isinstance()<python:isinstance>`.
        <BLANKLINE>
        <BLANKLINE>
        Keyword Arguments
        -----------------
        invert : :class:`bool`
            If :data:`True`, invert the output of the assertion:
            :code:`assert not isinstance(obj, class_or_tuple)`.
        <BLANKLINE>
        exception : :class:`type` [:exc:`Exception`], optional
            Assert that **exception** is raised during/before the assertion operation.
        <BLANKLINE>
        post_process : :data:`Callable[[Any], bool]<typing.Callable>`, optional
            Apply post-processing to the to-be asserted data before asserting aforementioned data.
            Example values would be the likes of :func:`any()<python:any>` and :func:`all()<python:all>`.
        <BLANKLINE>
        message : :class:`str`, optional
            A custom error message to-be passed to the ``assert`` statement.
        <BLANKLINE>
        <BLANKLINE>
        :rtype: :data:`None`
        <BLANKLINE>
        See also
        --------
        :func:`isinstance()<python:isinstance>`
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

    """  # noqa: E501
    try:
        __sgn = signature(func)
        sgn = Signature(_to_positional(__sgn.parameters.values()), return_annotation=None)
    except ValueError:
        sgn = Signature(parameters=DEFAULT_PRM, return_annotation=None)
        sgn_str = '(*args, **kwargs)'
    else:
        kv = sgn.parameters.items()
        sgn_str = '(' + ', '.join((k if v.default is _empty else f'{k}={k}') for k, v in kv) + ')'

    indent = 4 * ' '

    name = getattr(func, '__qualname__', func.__name__)
    domain = get_sphinx_domain(func)
    _summary = textwrap.dedent(indent + (func.__doc__ or 'No description.'))
    summary = textwrap.indent(_summary, indent)

    parameters = ''
    for k, v in sgn.parameters.items():
        prm_type = PARAM_NAME_MAPPING[v.kind]
        parameters += f'{k}\n    The {prm_type} argument ``{k}`` of {domain}.\n\n'

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
    return isbuiltin(func) and '.' not in getattr(func, '__qualname__', '')


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
    try:
        name: str = getattr(func, '__qualname__', func.__name__)
    except AttributeError as ex:
        raise TypeError("'func' expects a callable with the '__name__' attribute; "
                        f"observed type: {func.__class__.__name__!r}") from ex

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
    if module != 'builtins':
        return f':{directive}:`~{module}.{name}`'
    else:
        parenthesis = '()' if directive in {'func', 'meth'} else ''
        return f':{directive}:`{name}{parenthesis}<python:{name}>`'


#: An immutable mapping of to-be replaced substrings and their replacements.
README_MAPPING: Mapping[str, str] = MappingProxyType({
    '``': '|',
    '()': ''
})


def load_readme(readme: Union[str, bytes, int, os.PathLike],
                replace: Mapping[str, str] = README_MAPPING,
                **kwargs: Any) -> str:
    r"""Load and return the content of a readme file located in the same directory as this file.

    Equivalent to importing the content of ``../README.rst``.

    Parameters
    ----------
    readme : :class:`str`
        The name of the readme file.

    replace : :class:`~Collections.abc.Mapping` [:class:`str`, :class:`str`]
        A mapping of to-be replaced substrings contained within the readme file.

    \**kwargs : :data:`~typing.Any`
        Optional keyword arguments for :func:`open`.

    Returns
    -------
    :class:`str`
        The content of ``../README.rst``.

    """
    with open(readme, **kwargs) as f:
        ret: str = f.read()
    for old, new in replace.items():
        ret = ret.replace(old, new)
    return ret
