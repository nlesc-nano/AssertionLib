"""
assertionlib.dataclass
======================

A class with a number of generic pre-defined (magic) methods inspired by dataclass of Python 3.7.

Index
-----
.. currentmodule:: assertionlib.dataclass
.. autosummary::
    AbstractDataClass
    AbstractDataClass._PRIVATE_ATTR
    AbstractDataClass._HASHABLE
    AbstractDataClass.__str__
    AbstractDataClass._str_iterator
    AbstractDataClass.__eq__
    AbstractDataClass.__hash__
    AbstractDataClass.copy
    AbstractDataClass.__copy__
    AbstractDataClass.__deepcopy__
    AbstractDataClass.as_dict
    AbstractDataClass.from_dict
    AbstractDataClass.inherit_annotations

API
---
.. autoclass:: AbstractDataClass
.. autoattribute:: AbstractDataClass._PRIVATE_ATTR
.. autoattribute:: AbstractDataClass._HASHABLE
.. automethod:: AbstractDataClass.__str__
.. automethod:: AbstractDataClass._str_iterator
.. automethod:: AbstractDataClass.__eq__
.. automethod:: AbstractDataClass.__hash__
.. automethod:: AbstractDataClass.copy
.. automethod:: AbstractDataClass.__copy__
.. automethod:: AbstractDataClass.__deepcopy__
.. automethod:: AbstractDataClass.as_dict
.. automethod:: AbstractDataClass.from_dict
.. automethod:: AbstractDataClass.inherit_annotations

"""

import textwrap
import copy
from abc import ABCMeta
from typing import Any, Dict, Set, Iterable, Tuple
from contextlib import AbstractContextManager

__all__ = ['AbstractDataClass']


class IsOpen(AbstractContextManager):
    """A context manager for keeping track of recursive calls of a callable."""

    def __init__(self) -> None:
        self.is_open = False

    def __enter__(self) -> None:
        self.is_open = True

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.is_open = False

    def __bool__(self) -> bool:
        return self.is_open

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.is_open}>"


class _MetaADC(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs) -> type:
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        if cls._HASHABLE:  # Add the mcls.__hash__ method to cls if True
            setattr(cls, '__hash__', mcls._hash_template)
        return cls

    def _hash_template(self) -> int:
        """Return the hash of this instance.

        The returned hash is constructed from two components:
        * The hash of this instances' class type.
        * The hashes of all key/value pairs in this instances' (non-private) attributes.


        If an unhashable instance attribute is encountered, *e.g.* a :class:`list`,
        then its :func:`id` is used for hashing.

        This method will raise a :exc:`TypeError` if the class attribute
        :attr:`AbstractDataClass._HASHABLE` is ``False``.

        See Also
        --------

        :attr:`AbstractDataClass._PRIVATE_ATTR`:
            A :class:`set` with the names of private instance variables.

        :attr:`AbstractDataClass._HASHABLE`:
            Whether or not this class is hashable.

        :attr:`AbstractDataClass._hash_open`:
            A context manager for preventing recursive calls to this method.

        :attr:`AbstractDataClass._hash`:
            An instance variable for caching the :func:`hash` of this instance.

        """
        if self._hash:  # Return a cached hash
            return self._hash
        elif self._hash_open:  # Return the ID of this instance
            return id(self)

        # A precaution against recursive __hash__ calls
        with self._hash_open:
            ret = hash(type(self))
            for k, v in vars(self).items():
                if k in self._PRIVATE_ATTR:
                    continue
                try:
                    ret ^= hash((k, v))
                except TypeError:
                    ret ^= hash((k, id(v)))

            # Cache the hash and return
            self._hash = ret
            return ret


class AbstractDataClass(metaclass=_MetaADC):
    """A dataclass with a number of generic pre-defined (magic) methods."""

    #: A :class:`set` with the names of private instance variables.
    #: These attributes will be excluded whenever calling :meth:`AbstractDataClass.as_dict`,
    #: printing or comparing objects.
    _PRIVATE_ATTR: Set[str] = frozenset()

    #: Whether or not this class is hashable.
    #: If ``False``, raise a :exc:`TypeError` when calling :meth:`AbstractDataClass.__hash__`.
    _HASHABLE: bool = True

    def __init__(self) -> None:
        """Initialize a :class:`AbstractDataClass` instance."""
        # Assign cls._PRIVATE_ATTR as a (unfrozen) set to this instance as attribute
        cls = type(self)
        self._PRIVATE_ATTR = {'_PRIVATE_ATTR', '_repr_open', '_eq_open'}.union(cls._PRIVATE_ATTR)

        # Context managers for saveguarding against recursive method calls
        self._repr_open: AbstractContextManager = IsOpen()
        self._eq_open: AbstractContextManager = IsOpen()

        # Extra attributes in case the class is hashable
        if cls._HASHABLE:
            self._hash_open: AbstractContextManager = IsOpen()
            self._hash: int = 0
            self._PRIVATE_ATTR.add('_hash_open')
            self._PRIVATE_ATTR.add('_hash')

    def __repr__(self) -> str:
        """Return a string representation of this instance.

        The string representation consists of this instances' class name in addition
        to all (non-private) instance attributes.

        See Also
        --------
        :attr:`AbstractDataClass._PRIVATE_ATTR`:
            A :class:`set` with the names of private instance variables.

        :attr:`AbstractDataClass._repr_open`:
            A context manager for preventing recursive calls to this method.

        """
        def _str(k: str, v: Any) -> str:
            return f'{k:{width}} = ' + textwrap.indent(repr(v), indent2)[len(indent2):]

        # Return the hexed ID of this instance
        if self._repr_open:
            return object.__repr__(self).rstrip('>').rsplit(maxsplit=1)[1]

        # A precaution against recursive __repr__() calls
        with self._repr_open:
            try:
                width = max(len(k) for k in self._str_iterator())
            except ValueError:  # Raised if this instance has no instance attributes
                return f'{self.__class__.__name__}()'

            indent1 = ' ' * 4
            indent2 = ' ' * (3 + width)
            ret = ',\n'.join(_str(k, v) for k, v in self._str_iterator())

            return f'{self.__class__.__name__}(\n{textwrap.indent(ret, indent1)}\n)'

    def _str_iterator(self) -> Iterable[Tuple[str, Any]]:
        """Return an iterable for the :meth:`AbstractDataClass.__repr__` method."""
        return ((k, v) for k, v in vars(self).items() if k not in self._PRIVATE_ATTR)

    def __eq__(self, value: Any) -> bool:
        """Check if this instance is equivalent to **value**.

        The comparison checks if the class type of this instance and **value** are identical
        and if all (non-private) instance variables are equivalent.

        See Also
        --------
        :attr:`AbstractDataClass._PRIVATE_ATTR`:
            A :class:`set` with the names of private instance variables.

        :attr:`AbstractDataClass._eq_open`:
            A context manager for preventing recursive calls to this method.

        """
        # Compare the IDs' of this instance and value
        if self._eq_open:
            return id(self) == id(value)

        # Compare instance types
        if type(self) is not type(value):
            return False

        # A precaution against recursive __eq__ calls
        with self._eq_open:
            # Compare instance attributes
            try:
                for k, v1 in vars(self).items():
                    if k in self._PRIVATE_ATTR:
                        continue
                    v2 = getattr(value, k)
                    assert v1 == v2
            except (AttributeError, AssertionError):
                return False
            else:
                return True

    def copy(self, deep: bool = False) -> 'AbstractDataClass':
        """Return a deep or shallow copy of this instance.

        Parameters
        ----------
        deep : :class:`bool`
            Whether or not to return a deep or shallow copy.

        Returns
        -------
        :class:`AbstractDataClass`
            A new instance constructed from this instance.

        """
        cls = type(self)
        ret = cls.__new__(cls)
        ret.__dict__ = vars(self).copy() if not deep else copy.deepcopy(vars(self))
        return ret

    def __copy__(self) -> 'AbstractDataClass':
        """Return a shallow copy of this instance; see :meth:`AbstractDataClass.copy`."""
        return self.copy(deep=False)

    def __deepcopy__(self, memo=None) -> 'AbstractDataClass':
        """Return a deep copy of this instance; see :meth:`AbstractDataClass.copy`."."""
        return self.copy(deep=True)

    def as_dict(self, return_private: bool = False) -> Dict[str, Any]:
        """Construct a dictionary from this instance with all non-private instance variables.

        Parameters
        ----------
        return_private : :class:`bool`
            If ``True``, return both public and private instance variables.
            Private instance variables are defined in :data:`AbstractDataClass._PRIVATE_ATTR`.

        Returns
        -------
        :class:`dict` [:class:`str`, :data:`Any<typing.Any>`]
            A dictionary of arrays with keyword arguments for initializing a new
            instance of this class.

        See Also
        --------
        :meth:`AbstractDataClass.from_dict`:
            Construct a instance of this objects' class from a dictionary with keyword arguments.

        :attr:`AbstractDataClass._PRIVATE_ATTR`:
            A :class:`set` with the names of private instance variables.

        """
        skip_attr = self._PRIVATE_ATTR if not return_private else set()
        return {k: copy.copy(v) for k, v in vars(self).items() if k not in skip_attr}

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> 'AbstractDataClass':
        """Construct a instance of this objects' class from a dictionary with keyword arguments.

        Parameters
        ----------
        dct : :class:`dict` [:class:`str`, :data:`Any<typing.Any>`]
            A dictionary with keyword arguments for constructing a new
            :class:`AbstractDataClass` instance.

        Returns
        -------
        :class:`AbstractDataClass`
            A new instance of this object's class constructed from **dct**.

        See Also
        --------
        :meth:`AbstractDataClass.as_dict`:
            Construct a dictionary from this instance with all non-private instance variables.

        """
        return cls(**dct)

    @classmethod
    def inherit_annotations(cls) -> type:
        """A decorator for inheriting annotations and docstrings.

        Can be applied to methods of :class:`AbstractDataClass` subclasses to automatically
        inherit the docstring and annotations of identical-named functions of its superclass.

        References to :class:`AbstractDataClass` are replaced with ones pointing to the
        respective subclass.

        Examples
        --------
        .. code:: python

            >>> class SubClass(AbstractDataClass):
            ...
            ...     @AbstractDataClass.inherit_annotations()
            ...     def __copy__(self): pass

            >>> print(SubClass.__copy__.__doc__)
            Return a shallow copy of this instance; see :meth:`SubClass.copy`.

            >>> print(SubClass.__copy__.__annotations__)
            {'return': 'SubClass'}

        """
        def decorator(func: type) -> type:
            cls_func = getattr(cls, func.__name__)
            sub_cls_name = func.__qualname__.split('.')[0]

            # Update annotations
            if not func.__annotations__:
                func.__annotations__ = dct = getattr(cls_func, '__annotations__', {}).copy()
                if 'return' in dct and dct['return'] in (cls, cls.__name__):
                    dct['return'] = sub_cls_name

            # Update docstring
            if func.__doc__ is None:
                func.__doc__ = cls_func.__doc__.replace(cls.__name__, sub_cls_name)

            return func
        return decorator
