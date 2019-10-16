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
    AbstractDataClass.__str__
    AbstractDataClass._str_iterator
    AbstractDataClass.__eq__
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
.. automethod:: AbstractDataClass.__str__
.. automethod:: AbstractDataClass._str_iterator
.. automethod:: AbstractDataClass.__eq__
.. automethod:: AbstractDataClass.copy
.. automethod:: AbstractDataClass.__copy__
.. automethod:: AbstractDataClass.__deepcopy__
.. automethod:: AbstractDataClass.as_dict
.. automethod:: AbstractDataClass.from_dict
.. automethod:: AbstractDataClass.inherit_annotations

"""

import textwrap
from copy import deepcopy
from typing import (Any, Dict, FrozenSet, Iterable, Tuple)


class AbstractDataClass:
    """A dataclass with a number of generic pre-defined (magic) methods."""

    #: A :class:`frozenset` with the names of private instance variables.
    #: These attributes will be excluded whenever calling :meth:`AbstractDataClass.as_dict`,
    #: printing or comparing objects.
    _PRIVATE_ATTR: FrozenSet[str] = frozenset()

    def __str__(self) -> str:
        """Return a string representation of this instance."""
        def _str(k: str, v: Any) -> str:
            return f'{k:{width}} = ' + textwrap.indent(repr(v), indent2)[len(indent2):]

        width = max(len(k) for k in vars(self) if k not in self._PRIVATE_ATTR)
        indent1 = ' ' * 4
        indent2 = ' ' * (3 + width)
        iterable = self._str_iterator()
        ret = ',\n'.join(_str(k, v) for k, v in iterable)

        return f'{self.__class__.__name__}(\n{textwrap.indent(ret, indent1)}\n)'

    __repr__ = __str__

    def _str_iterator(self) -> Iterable[Tuple[str, Any]]:
        """Return an iterable for the :meth:`AbstractDataClass.__str__` method."""
        return ((k, v) for k, v in vars(self).items() if k not in self._PRIVATE_ATTR)

    def __eq__(self, value: Any) -> bool:
        """Check if this instance is equivalent to **value**.

        The comparison checks if the class type of this instance and **value** are identical
        and if all (non-private) instance variables are equivalent.

        """
        # Compare instance types
        if type(self) is not type(value):
            return False

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

    def __hash__(self) -> int:
        """Return the hash of this instance.

        The returned hash is constructed from two components:
        * The hash of this instances' class type.
        * The hashes of all key/value pairs in this instances' attributes.

        If an unhashable instance attribute is encountered, *e.g.* a :class:`list`,
        then its :func:`id` is used for hashing.

        """
        ret = hash(type(self))
        for k, v in vars(self).items():
            if k in self._PRIVATE_ATTR:
                continue
            try:
                ret ^= hash((k, v))
            except TypeError:
                ret ^= hash((k, id(v)))
        return ret

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
        ret.__dict__ = vars(self).copy() if not deep else deepcopy(vars(self))
        return ret

    def __copy__(self) -> 'AbstractDataClass':
        """Return a shallow copy of this instance; see :meth:`AbstractDataClass.copy`."""
        return self.copy(deep=False)

    def __deepcopy__(self, memo=None) -> 'AbstractDataClass':
        """Return a deep copy of this instance; see :meth:`AbstractDataClass.copy`."."""
        return self.copy(deep=True)

    def as_dict(self, return_private: bool = False) -> Dict[str, Any]:
        """Construct a dictionary from this instance with all non-private instance variables.

        No attributes specified in :data:`AbstractDataClass._PRIVATE_ATTR` will be included in
        the to-be returned dictionary.

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

        """
        ret = deepcopy(vars(self))
        if not return_private:
            for key in self._PRIVATE_ATTR:
                del ret[key]
        return ret

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
                func.__annotations__ = dct = cls_func.__annotations__.copy()
                if 'return' in dct and dct['return'] in (cls, cls.__name__):
                    dct['return'] = sub_cls_name

            # Update docstring
            if func.__doc__ is None:
                func.__doc__ = cls_func.__doc__.replace(cls.__name__, sub_cls_name)

            return func
        return decorator
