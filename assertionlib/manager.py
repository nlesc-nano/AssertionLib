"""
assertionlib.manager
====================

A module containing the actual :class:`AssertionManager` class.

Index
-----
.. currentmodule:: assertionlib.manager
.. autosummary::
    assertion
    AssertionManager
    AssertionManager.assert_
    AssertionManager.__call__
    AssertionManager.add_to_instance

Assertions based on the builtin :mod:`operator` module.

.. autosummary::
    :nosignatures:

    AssertionManager.abs
    AssertionManager.add
    AssertionManager.and_
    AssertionManager.concat
    AssertionManager.contains
    AssertionManager.countOf
    AssertionManager.eq
    AssertionManager.floordiv
    AssertionManager.ge
    AssertionManager.getitem
    AssertionManager.gt
    AssertionManager.index
    AssertionManager.indexOf
    AssertionManager.inv
    AssertionManager.invert
    AssertionManager.is_
    AssertionManager.is_not
    AssertionManager.le
    AssertionManager.lshift
    AssertionManager.lt
    AssertionManager.matmul
    AssertionManager.mod
    AssertionManager.mul
    AssertionManager.ne
    AssertionManager.neg
    AssertionManager.not_
    AssertionManager.or_
    AssertionManager.pos
    AssertionManager.pow
    AssertionManager.rshift
    AssertionManager.sub
    AssertionManager.truediv
    AssertionManager.truth

Assertions based on the builtin :mod:`os.path` module.

.. autosummary::
    :nosignatures:

    AssertionManager.isabs
    AssertionManager.isdir
    AssertionManager.isfile
    AssertionManager.islink
    AssertionManager.ismount

Assertions based on the builtin :mod:`math` module.

.. autosummary::
    :nosignatures:

    AssertionManager.allclose
    AssertionManager.isclose
    AssertionManager.isfinite
    AssertionManager.isinf
    AssertionManager.isnan

Assertions based on the builtin :mod:`builtins` module.

.. autosummary::
    :nosignatures:

    AssertionManager.callable
    AssertionManager.hasattr
    AssertionManager.isinstance
    AssertionManager.issubclass
    AssertionManager.len
    AssertionManager.any
    AssertionManager.all


Miscellaneous assertions.

.. autosummary::
    :nosignatures:

    AssertionManager.allclose
    AssertionManager.len_eq
    AssertionManager.str_eq
    AssertionManager.shape_eq
    AssertionManager.function_eq

API
---
.. autodata:: assertion
    :annotation: : AssertionManager

.. autoclass:: AssertionManager
.. automethod:: AssertionManager.assert_
.. automethod:: AssertionManager.__call__
.. automethod:: AssertionManager.add_to_instance

Assertions based on the builtin :mod:`operator` module
------------------------------------------------------
.. automethod:: AssertionManager.abs
.. automethod:: AssertionManager.add
.. automethod:: AssertionManager.and_
.. automethod:: AssertionManager.concat
.. automethod:: AssertionManager.contains
.. automethod:: AssertionManager.countOf
.. automethod:: AssertionManager.eq
.. automethod:: AssertionManager.floordiv
.. automethod:: AssertionManager.ge
.. automethod:: AssertionManager.getitem
.. automethod:: AssertionManager.gt
.. automethod:: AssertionManager.index
.. automethod:: AssertionManager.indexOf
.. automethod:: AssertionManager.inv
.. automethod:: AssertionManager.invert
.. automethod:: AssertionManager.is_
.. automethod:: AssertionManager.is_not
.. automethod:: AssertionManager.le
.. automethod:: AssertionManager.lshift
.. automethod:: AssertionManager.lt
.. automethod:: AssertionManager.matmul
.. automethod:: AssertionManager.mod
.. automethod:: AssertionManager.mul
.. automethod:: AssertionManager.ne
.. automethod:: AssertionManager.neg
.. automethod:: AssertionManager.not_
.. automethod:: AssertionManager.or_
.. automethod:: AssertionManager.pos
.. automethod:: AssertionManager.pow
.. automethod:: AssertionManager.rshift
.. automethod:: AssertionManager.sub
.. automethod:: AssertionManager.truediv
.. automethod:: AssertionManager.truth

Assertions based on the builtin :mod:`os.path` module
-----------------------------------------------------
.. automethod:: AssertionManager.isabs
.. automethod:: AssertionManager.isdir
.. automethod:: AssertionManager.isfile
.. automethod:: AssertionManager.islink
.. automethod:: AssertionManager.ismount

Assertions based on the builtin :mod:`math` module
--------------------------------------------------
.. automethod:: AssertionManager.allclose
.. automethod:: AssertionManager.isclose
.. automethod:: AssertionManager.isfinite
.. automethod:: AssertionManager.isinf
.. automethod:: AssertionManager.isnan

Assertions based on the builtin :mod:`builtins` module
------------------------------------------------------
.. automethod:: AssertionManager.callable
.. automethod:: AssertionManager.hasattr
.. automethod:: AssertionManager.isinstance
.. automethod:: AssertionManager.issubclass
.. automethod:: AssertionManager.len
.. automethod:: AssertionManager.any
.. automethod:: AssertionManager.all

Miscellaneous assertions
------------------------
.. automethod:: AssertionManager.allclose
.. automethod:: AssertionManager.len_eq
.. automethod:: AssertionManager.str_eq
.. automethod:: AssertionManager.shape_eq
.. automethod:: AssertionManager.function_eq

"""

import os
import sys
import math
import inspect
import reprlib
import builtins
import textwrap
import operator
from types import MappingProxyType
from inspect import Parameter
from string import ascii_lowercase
from typing import (Callable, Any, Type, Set, Optional, Mapping, Sequence, cast, Iterable,
                    FrozenSet, TypeVar)

from .ndrepr import aNDRepr
from .functions import bind_callable, len_eq, str_eq, shape_eq, function_eq
from .dataclass import AbstractDataClass, _MetaADC

if sys.version_info <= (3, 6):
    COMMA = ','
else:
    COMMA = ''

__all__ = ['AssertionManager', 'assertion']

T = TypeVar('T')


def return_value(value: T) -> T:
    """Return the supplied **value** in unaltered form."""
    return value


return_value.__name__ = return_value.__qualname__ = ''


class _MetaAM(_MetaADC):
    """The meta-class of :class:`AssertionManager`.

    The :meth:`_MetaAM.__new__` method iterates over (almost) all functions in the :mod:`operator`
    module and binds a matching assertion method to the :class:`AssertionManager` class.

    """

    #: A :class:`frozenset` of to-be ignored functions in :mod:`operator`.
    EXCLUDE: FrozenSet[str] = frozenset({
        'setitem', 'delitem', 'attrgetter', 'methodcaller', 'itemgetter', 'length_hint'
    })

    #: A :class:`frozenset` of callables which need an assertion function.
    INCLUDE: FrozenSet[Callable] = frozenset({
        os.path.isfile, os.path.isdir, os.path.isabs, os.path.islink, os.path.ismount,
        math.isclose, math.isfinite, math.isinf, math.isnan,
        isinstance, issubclass, callable, hasattr, len, bool, any, all,
        len_eq, str_eq, shape_eq, function_eq
    })

    def __new__(mcls, name, bases, namespace) -> '_MetaAM':  # noqa: N804
        cls = cast('_MetaAM', super().__new__(mcls, name, bases, namespace))

        operator_set: Set[str] = set(operator.__all__) - mcls.EXCLUDE  # type: ignore

        # Iterature over the __all__ attribute of the operator builtin module
        for name in operator_set:
            func: Callable = getattr(operator, name)
            bind_callable(cls, func, name)

        # Iterate over all remaining callables
        for func in mcls.INCLUDE:
            bind_callable(cls, func)

        cls.allclose = cls.isclose  # type: ignore

        # On windows os.path.isdir is an alias for the ._isdir function
        if os.name == 'nt':
            cls.isdir = cls._isdir  # type: ignore
            cls.isdir.__name__ = 'isdir'  # type: ignore
            cls.isdir.__qualname__ = 'isdir'  # type: ignore
            cls.isdir.__doc__ = cls.isdir.__doc__.replace('_isdir', 'isdir')  # type: ignore
            del cls._isdir  # type: ignore
        return cls


class _Str:
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)


class _NoneException(Exception):
    """An empty exception used by :meth:`AssertionManager.assert_` incase the **exception** parameter is ``None``."""  # noqa


class AssertionManager(AbstractDataClass, metaclass=_MetaAM):
    """A class for performing assertions and providing informative exception messages.

    A number of usage examples are provided in the the documentation_.

    .. _documentation: https://assertionlib.readthedocs.io/en/latest/includeme.html#usage

    Parameters
    ----------
    repr_instance : :class:`reprlib.Repr`, optional
        An instance of :class:`reprlib.Repr` for formatting Exception messages.
        The passed instance should have access to a bound callable by the name of ``repr``,
        which in turn should produce a string representation of any passed objects.
        If ``None``, default the builtin :func:`repr` function.
        See also :attr:`AssertionManager.repr_instance`.

    Attributes
    ----------
    repr_instance : :class:`reprlib.Repr`, optional
        An instance of :class:`reprlib.Repr` for formatting Exception messages.
        The passed instance should have access to a bound callable by the name of ``repr``,
        which in turn should produce a string representation of passed objects.
        If ``None``, default the builtin :func:`repr` function.

    _repr_fallback : :class:`Callable[[Any], str]<collections.abc.Callable>`
        A fallback value in case :attr:`AssertionManager.repr_instance` is ``None``.

    _maxstring_fallback : :class:`int`
        A fallback value in case :attr:`AssertionManager.repr_instance` is ``None``.

    """

    _PRIVATE_ATTR: Set[str] = frozenset({'_repr_fallback', '_maxstring_fallback'})  # type: ignore

    def __init__(self, repr_instance: Optional[reprlib.Repr] = aNDRepr) -> None:
        """Initialize an :class:`AssertionManager` instance."""
        super().__init__()
        self.repr_instance = repr_instance

        # Back values for AssertionManager.repr and AssertionManager.maxstring
        # Used when repr_instance is None
        self._repr_fallback: Callable[[Any], str] = builtins.repr
        self._maxstring_fallback = 80

    @property
    def repr(self) -> Callable[[Any], str]:
        """Return the :meth:`~reprlib.Repr.repr` method of :attr:`AssertionManager.repr_instance`."""  # noqa
        try:
            return self.repr_instance.repr  # type: ignore
        except AttributeError:  # If self.repr_instance is None
            return self._repr_fallback

    @property
    def maxstring(self) -> int:
        """Return the :attr:`~reprlib.Repr.maxstring` attribute of :attr:`AssertionManager.repr_instance`."""  # noqa
        try:
            return self.repr_instance.maxstring  # type: ignore
        except AttributeError:  # If self.repr_instance is None
            return self._maxstring_fallback

    # Public methods

    def assert_(self, func: Callable[..., T], *args: Any, invert: bool = False,
                exception: Optional[Type[Exception]] = None,
                post_process: Optional[Callable[[T], Any]] = None,
                message: Optional[str] = None,
                **kwargs: Any) -> None:
        r"""Perform the following assertion: :code:`assert func(*args, **kwargs)`.

        Examples
        --------
        For example :code:`assert 5 == 5` is equivalent to
        :code:`AssertionManager().assert_(operator.eq, 5, 5)`.

        Parameters
        ----------
        func : :class:`Callable[..., T]<collections.abc.Callable>`
            The callable whose output will be evaluated.

        \*args : :data:`~typing.Any`
            Positional arguments for **func**.

        invert : :class:`bool`
            If ``True``, invert the output of the assertion:
            :code:`assert not func(*args, **kwargs)`.

        exception : :class:`type` [:exc:`Exception`], optional
            Assert that **exception** is raised during/before the assertion operation.
            The only dissalowed value is :exc:`AssertionError`.

        post_process : :class:`Callable[[T], Any]<collections.abc.Callable>`, optional
            Apply post-processing to the to-be asserted data before asserting aforementioned data.
            Example functions would be the likes of :func:`any()<python:any>` and
            :func:`all()<python:all>`.

        message : :data:`~typing.Any`, optional
            A custom error message to-be passed to the ``assert`` statement.

        \**kwargs : :class:`str`, optional
            Keyword arguments for **func**.


        :rtype: :data:`None`

        See Also
        --------
        :meth:`AssertionManager.__call__`
            Equivalent to :code:`assert value`.

        """
        __tracebackhide__ = True

        # Set exception to _NoneException
        exception_ = cast(Type[Exception], _NoneException if exception is None else exception)

        if not (isinstance(exception_, type) and issubclass(exception_, Exception)):
            raise TypeError("'exception' expected 'None' or an Exception type; "
                            f"observed {self.repr(exception)} "
                            f"of type {exception.__class__.__name__!r}")
        elif exception_ is AssertionError:
            raise ValueError("'AssertionError' is not allowed as value "
                             "for the 'exception' parameter")

        output: Any = None
        try:
            if invert:
                output = not func(*args, **kwargs)
            else:
                output = func(*args, **kwargs)

            if post_process is None:
                assert output, message
            else:
                assert post_process(output), message

            if exception_ is not _NoneException:  # i.e. the exception parameter is not None
                message_ = f"Failed to raise {exception_.__name__!r}"
                if message is not None:
                    message_ += f'; {message}'
                raise AssertionError(message_)

        except exception_:  # This is the expected exception
            pass  # Not relevant if the exception parameter is None

        except Exception as ex:  # This is an unexpected exception
            exc = AssertionError(self._get_exc_message(
                ex, func, *args, output=output, invert=invert,
                post_process=post_process, **kwargs
            ))

            if type(ex) is AssertionError:
                exc.__cause__ = None
                raise exc
            else:
                raise exc from ex

    def __call__(self, value: T, invert: bool = False,
                 post_process: Optional[Callable[[T], Any]] = None,
                 message: Optional[str] = None) -> None:
        return self.assert_(return_value, value, invert=invert,
                            post_process=post_process, message=message)

    __call__.__doc__ = f"""Equivalent to :code:`assert value`.

        Examples
        --------
        .. code:: python

            >>> from assertionlib import assertion

            >>> assertion(5 == 5)
            >>> assertion(5 == 6)
            Traceback (most recent call last):
              ...
            AssertionError: output = (value); assert output
            <BLANKLINE>
            exception: AssertionError = AssertionError(None{COMMA})
            <BLANKLINE>
            output: bool = False
            value: bool = False


        Parameters
        ----------
        value : :data:`T<typing.Any>`
            The to-be asserted value.

        invert : :class:`bool`
            If ``True``, invert the output of the assertion:
            :code:`assert not value`.

        post_process : :class:`Callable[[T], Any]<collections.abc.Callable>`, optional
            Apply post-processing to the to-be asserted data before asserting aforementioned data.
            Example functions would be the likes of :func:`any()<python:any>` and
            :func:`all()<python:all>`.

        message : :class:`str`, optional
            A custom error message to-be passed to the ``assert`` statement.


        :rtype: :data:`None`

        """

    def add_to_instance(self, func: Callable, name: Optional[str] = None,
                        override_attr: bool = False) -> None:
        """Add a new custom assertion method to this instance.

        The new method name is added to :attr:`AssertionManager._PRIVATE_ATTR`.

        Parameters
        ----------
        func : :class:`~collections.abc.Callable`
            The callable whose output will be asserted in the to-be created method.

        name : :class:`str`, optional
            The name of the new method.
            If ``None``, use the name of **func**.

        override_attr : :class:`bool`
            If ``False``, raise an :exc:`AttributeError` if a method with the same name already
            exists in this instance.


        :rtype: :data:`None`

        Raises
        ------
        AttributeError
            Raised if ``override_attr=False`` and a method with the same name already
            exists in this instance.

        """
        name = name if name is not None else func.__name__
        if not override_attr and hasattr(self, name):
            raise AttributeError(f"{self.__class__.__name__!r} instance already has an attribute "
                                 f"by the name of {name!r}")
        bind_callable(self, func, name)

        # Add the name as private attribute
        self._PRIVATE_ATTR.add(name)

    # Private methods

    def _get_exc_message(self, ex: Exception, func: Callable[..., T], *args: Any,
                         invert: bool = False, output: Any = None,
                         post_process: Optional[Callable[[T], Any]] = None,
                         **kwargs: Any) -> str:
        __tracebackhide__ = True

        # Construct a string-reprensentation of the to-be assert function
        name: str = getattr(func, '__qualname__', func.__name__)

        # Construct a signature of the to-be asserted function
        try:
            _signature = inspect.signature(func)
            signature: Any = self._get_exc_signature(_signature, args, kwargs)
            parameters: Iterable = signature.parameters
        except ValueError:  # Not all callables have a signature
            signature = '(...)'
            parameters = (f'_{i}' for i in ascii_lowercase)

        not_ = '' if not invert else ' not'
        out = 'post_process(output)' if post_process is not None else 'output'
        ret = f'output ={not_} {name}{signature}; assert {out}'

        # Create a description of the exception
        ret += '\n\n' + self._get_prm_description('exception', ex)

        # Create a description of the to-be returned value
        ret += '\n\n' + self._get_prm_description('output', output)
        if post_process is not None:
            ret += '\n' + self._get_prm_description('post_process', post_process)

        # Create a description of positional arguments
        for key, value in zip(parameters, args):
            ret += '\n' + self._get_prm_description(key, value)

        # Create a description of keyword arguments
        for key, value in kwargs.items():
            ret += '\n' + self._get_prm_description(key, value)

        return ret

    _get_exc_message.__doc__ = f"""Return a formatted exception message for failed assertions.

        Examples
        --------
        .. code:: python

            >>> import operator

            >>> ex = TypeError('Fancy custom exception')
            >>> func = operator.contains
            >>> a = [1, 2, 3, 4]
            >>> b = 5

            >>> msg = assertion._get_exc_message(ex, func, a, b)
            >>> raise AssertionError(msg)
            Traceback (most recent call last):
              ...
            AssertionError: output = contains(a, b); assert output
            <BLANKLINE>
            exception: TypeError = TypeError('Fancy custom exception'{COMMA})
            <BLANKLINE>
            output: NoneType = None
            a: list = [1, 2, 3, 4]
            b: int = 5

        Parameters
        ----------
        ex : :class:`Exception`
            The exception raised by :meth:`AssertionManager.assert_`.

        func : :class:`~collections.abc.Callable`
            The callable whose output has been evaluated.

        \\*args : :data:`~typing.Any`
            Positional arguments supplied to **func**.

        invert : :class:`bool`
            If ``True``, invert the output of the assertion: :code:`not func(a, b, **kwargs)`.

        output : :data:`~typing.Any`, optional
            The output value of :code:`func(*args, **kwargs)` or :code:`not func(*args, **kwargs)`.

        post_process : :class:`~collections.abc.Callable`, optional
            Apply post-processing to the to-be asserted data before asserting aforementioned data.
            Example functions would be the likes of :func:`~builtins.any` and :func:`~builtins.all`.

        \\**kwargs : :data:`~typing.Any`, optional
            Further optional keyword arguments supplied to **func**.

        Returns
        -------
        :class:`str`
            A newly-formatted exception message to-be raised by :meth:`AssertionManager.assert_`.

        """  # noqa

    @staticmethod
    def _get_exc_signature(signature: inspect.Signature, args: Sequence[str],
                           kwargs: Mapping[str, Any] = MappingProxyType({})) -> inspect.Signature:
        """Create a new signature for the callable supplied to :meth:`AssertionManager._get_exc_message`.

        The return signature consists of two components:

        * The original positional/keyword arguments of the callables' signature (**signature**).
        * Extra positional/keyword arguments supplied to the callable.

        """  # noqa
        # Unpack parameters
        empty = inspect._empty  # type: ignore
        parameters = signature.parameters
        kind = Parameter.POSITIONAL_OR_KEYWORD

        # Create iterators over arguments
        prm_iter_args = (k for k, v in parameters.items() if v.default is empty)
        prm_iter_kwargs = ((k, v) for k, v in parameters.items() if v.default is not empty)
        args_iter = iter(args)

        # Add positional arguments
        param = [Parameter(name=k, kind=kind) for k, v in zip(prm_iter_args, args_iter)]
        param += [Parameter(name=f'_{k}', kind=kind) for k, _ in zip(ascii_lowercase, args_iter)]

        # Add keyword arguments
        param += [Parameter(name=k, kind=kind, default=v.default) for k, v in prm_iter_kwargs
                  if k not in kwargs]
        param += [Parameter(name=k, kind=kind, default=_Str(k)) for k in kwargs]
        return inspect.Signature(parameters=param, return_annotation=empty)

    def _get_prm_description(self, key: str, value: Any) -> str:
        """Construct a string representation of **key**/**value** pairs in :meth:`AssertionManager._get_exc_message`.

        The value will be placed on a newline of its string representation contains a
        newline character or is longer than :attr:`AssertionManager.maxstring`.

        """  # noqa
        _value_str = f'{self.repr(value)}' if not isinstance(value, Exception) else repr(value)
        key_str = f'{key}: {value.__class__.__name__} ='

        # Put the value on a newline if it is too long or contains a newline character
        condition = '\n' in _value_str or len(key_str) + len(_value_str) > self.maxstring
        if condition:  # Value is too long, put it on the next line
            indent = 4 * ' '
            value_str = f'\n{textwrap.indent(_value_str, indent)}'
        else:
            value_str = f' {_value_str}'

        return f'{key_str}{value_str}'


#: An instance of :class:`AssertionManager`.
assertion = AssertionManager()  # Type: Final[AssertionManager]
