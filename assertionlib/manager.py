"""
assertionlib.manager
====================

Various assertion-related classes for the testing of CAT.

Index
-----
.. currentmodule:: assertionlib.manager
.. autosummary::
    assertion
    AssertionManager
    _MetaAM

API
---
.. autodata:: assertion
    :annotation: = <AssertionManager object>

.. autoclass:: AssertionManager
    :members:
    :special-members:
    :private-members:

.. autoclass:: _MetaAM
    :members:
    :special-members:
    :private-members:

"""

import os
import reprlib
import builtins
import textwrap
import operator
from string import ascii_lowercase
from typing import Callable, Any, Type, FrozenSet, Optional

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
    EXCLUDE: FrozenSet[str] = frozenset({'setitem', 'delitem'})

    #: A :class:`frozenset` of callables which need an assertion function.
    INCLUDE: FrozenSet[Callable] = frozenset({
        os.path.isfile, os.path.isdir, isinstance, issubclass, callable, hasattr, len_eq, allclose
    })

    def __new__(cls, name, bases, namespace, **kwargs) -> type:
        sub_cls = super().__new__(cls, name, bases, namespace, **kwargs)

        # Iterature over the __all__ attribute of the operator builtin module
        for name in operator.__all__:
            if name[1:] in operator.__all__ or name in _MetaAM.EXCLUDE:
                pass  # Exclude inplace operations

            func = getattr(operator, name)
            bind_callable(sub_cls, func, name)

        for func in _MetaAM.INCLUDE:
            name = func.__name__
            bind_callable(sub_cls, func, name)

        return sub_cls


class AssertionManager(AbstractDataClass, metaclass=_MetaAM):
    """An assertion manager.

    Paramaters
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

    @property
    def repr(self) -> Callable[[Any], str]:
        """Return the :meth:`repr<reprlib.Repr.repr>` method of :attr:`AssertionManager.repr_instance`."""  # noqa
        try:
            return self.repr_instance.repr
        except AttributeError:  # If self.repr_instance is None
            return builtins.repr

    def _get_exc_message(self, ex: Exception, func: Callable, *args: Any,
                         invert: bool = False, **kwargs: Any) -> str:
        """Return a formatted exception message for failed assertions.

        Examples
        --------
        .. code:: python

            >>> import operator

            >>> ex = TypeError('Fancy custom exception')
            >>> func = operator.contains
            >>> a = [1, 2, 3, 4]
            >>> b = 5

            >>> assertion = AssertionManager()
            >>> msg = assertion._get_exc_message(ex, func, a, b)
            >>> raise AssertionError(msg)
            AssertionError: contains(a, b)
            Exception: TypeError('Fancy custom exception')

            Value a:
                [1, 2, 3, 4]

            Value b:
                5

        Parameters
        ----------
        ex : :class:`Exception`
            The exception raised by :meth:`AssertionManager.assert_`.

        func : :class:`Callable<typing.Callable>`
            The callable whose output has been evaluated.

        \*args : :class:`Any<typing.Any>`
            Positional arguments supplied to **func**.

        invert :class:`bool`
            If ``True``, invert the output of the assertion: :code:`not func(a, b, **kwargs)`.

        \**kwargs : :class:`Any<typing.Any>`, optional
            Further optional keyword arguments supplied to **func**.

        Returns
        -------
        :class:`str`
            A newly-formatted exception message to-be raised by :meth:`AssertionManager.assert_`.

        """  # noqa
        __tracebackhide__ = True

        # Construct a string-reprensentation of the to-be assert function
        name = func.__qualname__ if hasattr(func, '__qualname__') else func.__name__
        ret = f'{name}('
        for i, (_, j) in enumerate(zip(args, ascii_lowercase)):
            ret += f', {j}' if i >= 1 else j
        if kwargs:
            ret += ', **kwargs'
        ret += ')'

        if invert:
            ret = 'not ' + ret

        # Create the actual assertion information
        indent = 4 * ' '
        ret += f'\nException: {repr(ex)}'
        for i, j in zip(args, ascii_lowercase):
            ret += f'\n\nValue {j}:\n{textwrap.indent(self.repr(i), indent)}'

        return ret

    def assert_(self, func: Callable, *args: Any, invert: bool = False, **kwargs: Any) -> None:
        """Perform the :func:`assert` operation on the output of :code:`func(a, b, **kwargs)`.

        Examples
        --------
        For example :code:`assert 5 == 5` is equivalent to
        :code:`AssertionManager().assert_(operator.eq, 5, 5)`.

        Parameters
        ----------
        func : :class:`Callable<typing.Callable>`
            The callable whose output will be evaluated.

        \*args : :class:`Any<typing.Any>`
            Positional arguments for **func**.

        invert :class:`bool`
            If ``True``, invert the output of the assertion: :code:`not func(a, b, **kwargs)`.

        \**kwargs : :class:`Any<typing.Any>`, optional
            Keyword arguments for **func**.

        """  # noqa
        __tracebackhide__ = True

        try:
            if invert:
                assert not func(*args, **kwargs)
            else:
                assert func(*args, **kwargs)
        except Exception as ex:
            err = self._get_exc_message(ex, func, *args, invert=invert, **kwargs)
            raise AssertionError(err).with_traceback(ex.__traceback__)

    def add_to_instance(self, func: Callable, override_attr: bool = False,
                        name: Optional[str] = None) -> None:
        """Add a new custom assertion method to this instance.

        Parameters
        ----------
        func : :class:`Callable<typing.Callable>`
            The callable whose output will be asserted in the to-be created method.

        override_attr : :class:`bool`
            If ``False``, raise an :exc:`AttributeError` if a method with the same name already
            exists in this instance.

        name : :class:`str`, optional
            The name of the name of the new method.
            If ``None``, use the name of **func**.

        Exception
        ---------
        AttributeError
            Raised if ``override_attr=False`` and a method with the same name already
            exists in this instance.

        """
        meth_name = name if name is not None else func.__name__
        if not override_attr and hasattr(self, meth_name):
            raise AttributeError(f"'{self.__class__.__name__}' instance already has an attribute "
                                 f"by the name of '{meth_name}'")
        bind_callable(self, func, name)

    def exception(self, exception: Type[Exception], func: Callable,
                  *args: Any, **kwargs: Any) -> None:
        """Assert that **exception** is raised by :code:`func(*args, **kwargs)`.

        Parameters
        ----------
        exception : class`type` [:exc:`Exception`]
            An exception that should be raised by :code:`func(*args, **kwargs)`.
            Note: :exc:`AssertionError` is dissallowed as value.

        func : :class:`Callable<typing.Callable>`
            The callable whose output will be evaluated.

        \*args : :class:`Any<typing.Any>`
            Positional arguments for **func**.

        \**kwargs : :class:`Any<typing.Any>`, optional
            Keyword arguments for **func**.

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


#: An instance of :class:`AssertionManager`.
assertion: AssertionManager = AssertionManager()
