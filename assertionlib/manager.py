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
    AssertionManager.add_to_instance
    AssertionManager.exception

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
    AssertionManager.itemgetter
    AssertionManager.le
    AssertionManager.length_hint
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

Miscellaneous assertions.

.. autosummary::
    :nosignatures:

    AssertionManager.allclose
    AssertionManager.callable
    AssertionManager.hasattr
    AssertionManager.isinstance
    AssertionManager.issubclass
    AssertionManager.len
    AssertionManager.len_eq

API
---
.. autodata:: assertion
    :annotation: = <AssertionManager object>

.. autoclass:: AssertionManager
.. automethod:: AssertionManager.assert_
.. automethod:: AssertionManager.add_to_instance
.. automethod:: AssertionManager.exception

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
.. automethod:: AssertionManager.itemgetter
.. automethod:: AssertionManager.le
.. automethod:: AssertionManager.length_hint
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

Miscellaneous assertions
------------------------
.. automethod:: AssertionManager.allclose
.. automethod:: AssertionManager.callable
.. automethod:: AssertionManager.hasattr
.. automethod:: AssertionManager.isinstance
.. automethod:: AssertionManager.issubclass
.. automethod:: AssertionManager.len
.. automethod:: AssertionManager.len_eq

"""

import os
import inspect
import reprlib
import builtins
import textwrap
import operator
from string import ascii_lowercase
from typing import Callable, Any, Type, FrozenSet, Optional, Container, Mapping, Sequence

from .ndrepr import aNDRepr
from .functions import bind_callable, len_eq, allclose
from .dataclass import AbstractDataClass

__all__ = ['AssertionManager', 'assertion']


class _MetaAM(type):
    """The meta-class of :class:`AssertionManager`.

    The :meth:`_MetaAM.__new__` method iterates over (almost) all functions in the :mod:`operator`
    module and binds a matching assertion method to the :class:`AssertionManager` class.

    """

    #: A :class:`frozenset` of to-be ignored functions in :mod:`operator`.
    EXCLUDE: FrozenSet[str] = frozenset({'setitem', 'delitem', 'attrgetter', 'methodcaller'})

    #: A :class:`frozenset` of callables which need an assertion function.
    INCLUDE: FrozenSet[Callable] = frozenset({
        os.path.isfile, os.path.isdir, os.path.isabs, os.path.islink, os.path.ismount,
        isinstance, issubclass, callable, hasattr, len_eq, allclose, len, bool
    })

    def __new__(cls, name, bases, namespace, **kwargs) -> type:
        sub_cls = super().__new__(cls, name, bases, namespace, **kwargs)

        # Iterature over the __all__ attribute of the operator builtin module
        func_list = operator.__all__
        exclude = cls.EXCLUDE
        include = cls.INCLUDE
        for name in func_list:
            if name[1:] in func_list or name[1:] + '_' in func_list or name in exclude:
                continue  # Exclude inplace operations

            func = getattr(operator, name)
            bind_callable(sub_cls, func, name)

        for func in include:
            name = func.__name__
            bind_callable(sub_cls, func, name)

        return sub_cls


class _Str:
    def __init__(self, value: str) -> None: self.value = value
    def __repr__(self) -> str: return str(self.value)
    __str__ = __repr__


class AssertionManager(AbstractDataClass, metaclass=_MetaAM):
    """An assertion manager.

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

    """

    def __init__(self, repr_instance: Optional[reprlib.Repr] = aNDRepr) -> None:
        """Initialize an :class:`AssertionManager` instance."""
        self.repr_instance = repr_instance

        # Back values for AssertionManager.repr and AssertionManager.maxstring
        # Used when repr_instance is None
        self._repr_fallback = builtins.repr
        self._maxstring_fallback = 80

    @property
    def repr(self) -> Callable[[Any], str]:
        """Return the :meth:`repr<reprlib.Repr.repr>` method of :attr:`AssertionManager.repr_instance`."""  # noqa
        try:
            return self.repr_instance.repr
        except AttributeError:  # If self.repr_instance is None
            return self._repr_fallback

    @property
    def maxstring(self) -> int:
        """Return the :attr:`maxstring<reprlib.Repr.maxstring>` attribute of :attr:`AssertionManager.repr_instance`."""  # noqa
        try:
            return self.repr_instance.maxstring
        except AttributeError:  # If self.repr_instance is None
            return self._maxstring_fallback

    # Public methods

    def assert_(self, func: Callable, *args: Any, invert: bool = False, **kwargs: Any) -> None:
        """Perform the :func:`assert` operation on the output of :code:`func(a, b, **kwargs)`.

        Examples
        --------
        For example :code:`assert 5 == 5` is equivalent to
        :code:`AssertionManager().assert_(operator.eq, 5, 5)`.

        Parameters
        ----------
        func : :data:`Callable<typing.Callable>`
            The callable whose output will be evaluated.

        \*args : :data:`Any<typing.Any>`
            Positional arguments for **func**.

        invert : :class:`bool`
            If ``True``, invert the output of the assertion: :code:`not func(a, b, **kwargs)`.

        \**kwargs : :data:`Any<typing.Any>`, optional
            Keyword arguments for **func**.


        :rtype: :data:`None`

        """  # noqa
        __tracebackhide__ = True

        output = None
        try:
            if invert:
                output = not func(*args, **kwargs)
            else:
                output = func(*args, **kwargs)
            assert output
        except Exception as ex:
            err = self._get_exc_message(ex, func, *args, invert=invert, output=output, **kwargs)
            raise AssertionError(err).with_traceback(ex.__traceback__)

    def exception(self, exception: Type[Exception], func: Callable,
                  *args: Any, **kwargs: Any) -> None:
        """Assert that **exception** is raised by :code:`func(*args, **kwargs)`.

        Parameters
        ----------
        exception : :class:`type` [:exc:`Exception`]
            An exception that should be raised by :code:`func(*args, **kwargs)`.
            Note: :exc:`AssertionError` is dissallowed as value.

        func : :data:`Callable<typing.Callable>`
            The callable whose output will be evaluated.

        \*args : :data:`Any<typing.Any>`
            Positional arguments for **func**.

        \**kwargs : :data:`Any<typing.Any>`, optional
            Keyword arguments for **func**.


        :rtype: :data:`None`

        See also
        --------
        :exc:`Exception`
            Common base class for all non-exit exceptions.

        """  # noqa
        __tracebackhide__ = True

        if exception is AssertionError:  # AssertionError
            raise TypeError("'AssertionError' is a disallowed value for the 'exception' parameter")

        try:
            func(*args, **kwargs)
            raise AssertionError(f"Failed to raise '{exception.__name__}'")
        except exception:
            pass  # This is the expected exception
        except Exception as ex:  # This is an unexpected exception
            err = self._get_exc_message(ex, func, *args, **kwargs)
            raise AssertionError(err).with_traceback(ex.__traceback__)

    def add_to_instance(self, func: Callable, override_attr: bool = False,
                        name: Optional[str] = None) -> None:
        """Add a new custom assertion method to this instance.

        Parameters
        ----------
        func : :data:`Callable<typing.Callable>`
            The callable whose output will be asserted in the to-be created method.

        override_attr : :class:`bool`
            If ``False``, raise an :exc:`AttributeError` if a method with the same name already
            exists in this instance.

        name : :class:`str`, optional
            The name of the name of the new method.
            If ``None``, use the name of **func**.


        :rtype: :data:`None`

        Raises
        ------
        AttributeError
            Raised if ``override_attr=False`` and a method with the same name already
            exists in this instance.

        """
        meth_name = name if name is not None else func.__name__
        if not override_attr and hasattr(self, meth_name):
            raise AttributeError(f"'{self.__class__.__name__}' instance already has an attribute "
                                 f"by the name of '{meth_name}'")
        bind_callable(self, func, name)

    # Private methods

    def _get_exc_message(self, ex: Exception, func: Callable, *args: Any,
                         invert: bool = False, output: Any = None, **kwargs: Any) -> str:
        """Return a formatted exception message for failed assertions.

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
            AssertionError: output = contains(a, b); assert output

            exception: AssertionError = AssertionError()

            output: bool = False
            a: list = [1, 2, 3, 4]
            b: int = 5

        Parameters
        ----------
        ex : :class:`Exception`
            The exception raised by :meth:`AssertionManager.assert_`.

        func : :data:`Callable<typing.Callable>`
            The callable whose output has been evaluated.

        \*args : :data:`Any<typing.Any>`
            Positional arguments supplied to **func**.

        invert : :class:`bool`
            If ``True``, invert the output of the assertion: :code:`not func(a, b, **kwargs)`.

        output : :data:`Any<typing.Any>`, optional
            The output value of :code:`func(*args, **kwargs)` or :code:`not func(*args, **kwargs)`.

        \**kwargs : :data:`Any<typing.Any>`, optional
            Further optional keyword arguments supplied to **func**.

        Returns
        -------
        :class:`str`
            A newly-formatted exception message to-be raised by :meth:`AssertionManager.assert_`.

        """  # noqa
        __tracebackhide__ = True

        # Construct a string-reprensentation of the to-be assert function
        try:
            name = func.__qualname__
        except AttributeError:  # Not all callables have the __qualname__ attribute
            name = func.__name__

        # Construct a signature of the to-be asserted function
        try:
            _signature = inspect.signature(func)
            signature = self._update_signature(_signature, args, kwargs)
            parameters = signature.parameters
        except ValueError:  # Not all callables have a signature
            signature = '(...)'
            parameters = ascii_lowercase

        not_ = '' if not invert else ' not'
        ret = f'output ={not_} {name}{signature}; assert output'

        # Create a description of the exception
        ret += '\n\n' + self._get_prm_description('exception', ex)

        # Create a description of the to-be returned value
        ret += '\n\n' + self._get_prm_description('output', output)

        # Create a description of positional arguments
        for key, value in zip(parameters, args):
            ret += '\n' + self._get_prm_description(key, value)

        # Create a description of keyword arguments
        for key, value in kwargs.items():
            ret += '\n' + self._get_prm_description(key, value)

        return ret

    @staticmethod
    def _update_signature(signature: inspect.Signature, args: Sequence,
                          kwargs: Mapping = {}) -> inspect.Signature:
        """Take a signature and replace all default values if they are present in **kwargs**."""
        # Unpack parameters
        empty = inspect._empty
        Parameter = inspect.Parameter
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
        """Construct a string representation of **key**/**value** pairs."""
        _value_str = f'{self.repr(value)}' if not isinstance(value, Exception) else repr(value)
        key_str = f'{key}: {value.__class__.__name__} ='

        # Put the value on a newline if it is too long or contains a newline character
        condition = '\n' in _value_str or len(key_str) + len(_value_str) > self.maxstring
        if condition:
            indent = 4 * ' '
            value_str = f'\n{textwrap.indent(_value_str, indent)}'
        else:
            value_str = ' ' + _value_str

        return key_str + value_str


#: An instance of :class:`AssertionManager`.
assertion: AssertionManager = AssertionManager()
