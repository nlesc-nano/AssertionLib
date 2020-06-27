"""A class with a number of generic pre-defined (magic) methods inspired by dataclass of Python 3.7.

Index
-----
.. currentmodule:: assertionlib.dataclass
.. autosummary::
    AbstractDataClass
    AbstractDataClass.__repr__
    AbstractDataClass.__eq__
    AbstractDataClass.__hash__
    AbstractDataClass.__copy__
    AbstractDataClass.__deepcopy__
    AbstractDataClass.copy
    AbstractDataClass.as_dict
    AbstractDataClass.from_dict
    AbstractDataClass.inherit_annotations

API
---
.. autoclass:: AbstractDataClass
.. automethod:: AbstractDataClass.__repr__
.. automethod:: AbstractDataClass.__eq__
.. automethod:: AbstractDataClass.__hash__
.. automethod:: AbstractDataClass.__copy__
.. automethod:: AbstractDataClass.__deepcopy__
.. automethod:: AbstractDataClass.copy
.. automethod:: AbstractDataClass.as_dict
.. automethod:: AbstractDataClass.from_dict
.. automethod:: AbstractDataClass.inherit_annotations

"""  # noqa: E501

import textwrap
import copy
from abc import ABCMeta
from functools import wraps
from threading import get_ident
from typing import (
    Any, Dict, Set, Iterable, Tuple, ClassVar, NoReturn, cast, Iterator, Union,
    Callable, Optional, Mapping, TypeVar, Type
)

__all__ = ['AbstractDataClass']

T = TypeVar('T')
TT = TypeVar('TT', bound='_MetaADC')
AT = TypeVar('AT', bound='AbstractDataClass')
FT = TypeVar('FT', bound=Callable[..., Any])


def recursion_safeguard(fallback: FT) -> Callable[[FT], FT]:
    """Decorate a function such that it calls **fallback** in case of recursive calls.

    Implementation based on :func:`reprlib.recursive_repr`.

    """
    def decorating_function(user_function: FT) -> FT:
        running: Set[Tuple[int, int]] = set()

        @wraps(user_function)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            key = id(self), get_ident()
            if key in running:
                return fallback(self, *args, **kwargs)

            running.add(key)
            try:
                result = user_function(self, *args, **kwargs)
            finally:
                running.discard(key)
            return result
        return cast(FT, wrapper)
    return decorating_function


class _MetaADC(ABCMeta):
    _HASHABLE: bool = NotImplemented

    def __new__(mcls: Type[TT], name: str, bases: Tuple[type, ...],
                namespace: Dict[str, Any]) -> TT:
        cls = cast(TT, super().__new__(mcls, name, bases, namespace))
        if not cls._HASHABLE:
            setattr(cls, '__hash__', mcls._hash_template1)
        else:
            func = recursion_safeguard(cls._repr_fallback)(mcls._hash_template2)  # type: ignore
            setattr(cls, '__hash__', func)
        return cls

    @staticmethod
    def _hash_template1(self: 'AbstractDataClass') -> NoReturn:
        """Unhashable type; raise a :exc:`TypeError`."""
        raise TypeError(f"Unhashable type: {self.__class__.__name__!r}")

    @staticmethod
    def _hash_template2(self: 'AbstractDataClass') -> int:
        """Return the hash of this instance.

        The returned hash is constructed from two components:
        * The hash of this instances' class type.
        * The hashes of all key/value pairs in this instances' (non-private) attributes.

        If an unhashable instance variable is encountered, *e.g.* a :class:`list`,
        then its :func:`id` is used for hashing.

        This method will raise a :exc:`TypeError` if the class attribute
        :attr:`AbstractDataClass._HASHABLE` is :data:`False`.

        See Also
        --------
        :attr:`AbstractDataClass._PRIVATE_ATTR`
            A set with the names of private instance variables.

        :attr:`AbstractDataClass._HASHABLE`
            Whether or not this class is hashable.

        :attr:`AbstractDataClass._hash_fallback`
            Fallback function for :meth:`AbstractDataClass.__hash__` incase of recursive calls.

        :attr:`AbstractDataClass._hash`
            An instance variable for caching the :func:`hash` of this instance.

        """
        # Return a cached hash
        if self._hash:
            return self._hash

        ret = hash(type(self))
        for k, v in self._iter_attrs():
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
    """A dataclass with a number of generic pre-defined (magic) methods.

    Provides methods for:

    * String conversion: :meth:`AbstractDataClass.__repr__`.
    * Object comparisons: :meth:`AbstractDataClass.__eq__`.
    * Hash construction: :meth:`AbstractDataClass.__hash__`.
    * Copying: :meth:`AbstractDataClass.copy`, :meth:`AbstractDataClass.__copy__` and
      :meth:`AbstractDataClass.__deepcopy__`.
    * Dictionary interconversion: :meth:`AbstractDataClass.as_dict` and
      :meth:`AbstractDataClass.from_dict`.
    * Inherting method docstrings and annotations: :meth:`AbstractDataClass.inherit_annotations`.

    Attributes
    ----------
    _PRIVATE_ATTR : :class:`frozenset` [:class:`str`] or :class:`set` [:class:`str`]
        A class variable with the names of private instance variable.
        These attributes will be excluded whenever calling :meth:`AbstractDataClass.as_dict`,
        printing or comparing objects.
        The set is unfrozen (and added as instance variables)
        the moment a class instance is initiated.

    _HASHABLE : :class:`bool`
        A class variable denoting whether or not class instances are hashable.
        The :attr:`AbstractDataClass.__hash__` method will be unavailable if :data:`False`.

    _hash : :class:`int`
        An attribute for caching the :func:`hash` of this instance.
        Only available if :attr:`AbstractDataClass._HASHABLE` is :data:`True`.

    """

    #: A :class:`frozenset` with the names of private instance variables.
    #: These attributes will be excluded whenever calling :meth:`AbstractDataClass.as_dict`,
    #: printing or comparing objects.
    _PRIVATE_ATTR: Set[str] = frozenset()  # type: ignore

    #: Whether or not this class is hashable.
    #: If :data:`False`, raise a :exc:`TypeError` when calling :meth:`AbstractDataClass.__hash__`.
    _HASHABLE: ClassVar[bool] = True

    #: Empty slots which can be filled by subclasses.
    __slots__: Union[str, Iterable[str]] = ('__dict__',)

    __hash__: Callable[[type], Union[int, NoReturn]]

    def __init__(self) -> None:
        """Initialize a :class:`AbstractDataClass` instance."""
        # Assign cls._PRIVATE_ATTR as a (unfrozen) set to this instance as attribute
        cls = type(self)
        self._PRIVATE_ATTR = {'_PRIVATE_ATTR'}.union(cls._PRIVATE_ATTR)

        # Extra attributes in case the class is hashable
        if cls._HASHABLE:
            self._PRIVATE_ATTR.add('_hash')
            self._hash: int = 0

    def _iter_attrs(self) -> Iterator[Tuple[str, Any]]:
        """Return an iterator which iterates over this instance's attributes as key/value pairs.

        If all attributes are stored in the instance :attr:`~object.__dict__` then
        further alterations to this method are not necessary.

        If :attr:`~object.__slots__` are utilized for defining attributes then alterations
        will have to be made to this method, *e.g.*:

        .. code:: python

            >>> def _iter_attrs(self):
            ...     yield 'a', self.a
            ...     yield 'b', self.b
            ...     yield 'c', self.c

        """
        return iter(vars(self).items())

    def _hash_fallback(self) -> int:
        """Fallback function for :meth:`AbstractDataClass.__hash__` incase of recursive calls."""
        return id(self)

    def _repr_fallback(self) -> str:
        """Fallback function for :meth:`AbstractDataClass.__repr__` incase of recursive calls."""
        return object.__repr__(self).rstrip('>').rsplit(maxsplit=1)[1]

    @recursion_safeguard(fallback=_repr_fallback)  # type: ignore
    def __repr__(self) -> str:
        """Return a (machine readable) string representation of this instance.

        The string representation consists of this instances' class name in addition
        to all (non-private) instance variables.

        Returns
        -------
        :class:`str`
            A string representation of this instance.

        See Also
        --------
        :attr:`AbstractDataClass._PRIVATE_ATTR`
            A set with the names of private instance variables.

        :attr:`AbstractDataClass._repr_fallback`
            Fallback function for :meth:`AbstractDataClass.__repr__` incase of recursive calls.

        :meth:`AbstractDataClass._str_iterator`
            Return an iterable for the iterating over this instances' attributes.

        :meth:`AbstractDataClass._str`
            Returns a string representation of a single **key**/**value** pair.

        """
        try:
            width = max(len(k) for k, _ in self._str_iterator())
        except ValueError:  # Raised if this instance has no instance variables
            return f'{self.__class__.__name__}()'

        ret = ',\n'.join(self._str(k, v, width, 3+width) for k, v in self._str_iterator())

        indent = ' ' * 4
        return f'{self.__class__.__name__}(\n{textwrap.indent(ret, indent)}\n)'

    def _str_iterator(self) -> Iterable[Tuple[str, Any]]:
        """Return an iterable for the :meth:`AbstractDataClass.__repr__` method."""
        return ((k, v) for k, v in sorted(self._iter_attrs()) if k not in self._PRIVATE_ATTR)

    @staticmethod
    def _str(key: str, value: Any,
             width: Optional[int] = None,
             indent: Optional[int] = None) -> str:
        """Return a string representation of a single **key**/**value** pair."""
        key_str = f'{key} = ' if width is None else f'{key:{width}} = '
        if indent is not None:
            value_str = textwrap.indent(repr(value), ' ' * indent)[indent:]
        else:
            value_str = repr(value)
        return f'{key_str}{value_str}'  # e.g.: "key   =     'value'"

    def _eq_fallback(self, value: Any) -> bool:
        """Fallback function for :meth:`AbstractDataClass.__eq__` incase of recursive calls."""
        return self is value

    @recursion_safeguard(fallback=_eq_fallback)  # type: ignore
    def __eq__(self, value: Any) -> bool:
        """Check if this instance is equivalent to **value**.

        The comparison checks if the class type of this instance and **value** are identical
        and if all (non-private) instance variables are equivalent.

        Returns
        -------
        :class:`bool`
            Whether or not this instance and **value** are equivalent.

        See Also
        --------
        :attr:`AbstractDataClass._PRIVATE_ATTR`
            A set with the names of private instance variables.

        :attr:`AbstractDataClass._eq`
            Return if **v1** and **v2** are equivalent.

        :attr:`AbstractDataClass._eq_fallback`
            Fallback function for :meth:`AbstractDataClass.__eq__` incase of recursive calls.

        """
        # Compare instance types
        if type(self) is not type(value):
            return False

        # Compare instance variables
        try:
            for k, v1 in self._iter_attrs():
                if k in self._PRIVATE_ATTR:
                    continue
                v2 = getattr(value, k)
                assert self._eq(v1, v2)
        except (AttributeError, AssertionError):
            return False
        else:
            return True

    @staticmethod
    def _eq(v1: Any, v2: Any) -> bool:
        """Return if **v1** and **v2** are equivalent."""
        return cast(bool, v1 == v2)

    def copy(self: AT, deep: bool = False) -> AT:
        """Return a shallow or deep copy of this instance.

        Parameters
        ----------
        deep : :class:`bool`
            Whether or not to return a deep or shallow copy.

        Returns
        -------
        :class:`AbstractDataClass`
            A new instance constructed from this instance.

        """
        def return_arg(arg: T) -> T:
            return arg

        copy_func = cast(Callable[[T], T], copy.deepcopy if deep else return_arg)

        cls = type(self)
        ret: AT = cls.__new__(cls)
        for k, v in self._iter_attrs():
            setattr(ret, k, copy_func(v))
        return ret

    def __copy__(self: AT) -> AT:
        """Return a shallow copy of this instance; see :meth:`AbstractDataClass.copy`."""
        return self.copy(deep=False)

    def __deepcopy__(self: AT, memo: Optional[Dict[int, Any]] = None) -> AT:
        """Return a deep copy of this instance; see :meth:`AbstractDataClass.copy`."."""
        return self.copy(deep=True)

    def as_dict(self, return_private: bool = False) -> Dict[str, Any]:
        """Construct a dictionary from this instance with all non-private instance variables.

        The returned dictionary values are shallow copies.

        Parameters
        ----------
        return_private : :class:`bool`
            If :data:`True`, return both public and private instance variables.
            Private instance variables are defined in :data:`AbstractDataClass._PRIVATE_ATTR`.

        Returns
        -------
        :class:`dict` [:class:`str`, :data:`~typing.Any`]
            A dictionary with keyword arguments for initializing a new
            instance of this class.

        See Also
        --------
        :meth:`AbstractDataClass.from_dict`:
            Construct a instance of this objects' class from a dictionary with keyword arguments.

        :attr:`AbstractDataClass._PRIVATE_ATTR`:
            A set with the names of private instance variables.

        """
        if return_private:
            return {k: copy.copy(v) for k, v in self._iter_attrs()}
        else:
            return {k: copy.copy(v) for k, v in self._iter_attrs() if k not in self._PRIVATE_ATTR}

    @classmethod
    def from_dict(cls: Type[AT], dct: Mapping[str, Any]) -> AT:
        """Construct a instance of this objects' class from a dictionary with keyword arguments.

        Parameters
        ----------
        dct : :class:`~collections.abc.Mapping` [:class:`str`, :data:`~typing.Any`]
            A dictionary with keyword arguments for constructing a new
            :class:`AbstractDataClass` instance.

        Returns
        -------
        :class:`AbstractDataClass`
            A new instance of this object's class constructed from **dct**.

        See Also
        --------
        :meth:`AbstractDataClass.as_dict`
            Construct a dictionary from this instance with all non-private instance variables.

        """
        return cls(**dct)  # type: ignore

    @classmethod
    def inherit_annotations(cls) -> Callable[[FT], FT]:
        """A decorator for inheriting annotations and docstrings.

        Can be applied to methods of :class:`AbstractDataClass` subclasses to automatically
        inherit the docstring and annotations of identical-named functions of its superclass.

        References to :class:`AbstractDataClass` are replaced with ones pointing to the
        respective subclass.

        Returns
        -------
        :class:`type`
            A decorator for updating the annotations and docstring of a callable.

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
            {'self': ~AT, 'return': ~AT}

        """
        def decorator(func: FT) -> FT:
            cls_func: str = getattr(cls, func.__name__)
            sub_cls_name: str = func.__qualname__.split('.')[0]

            # Update annotations
            if not getattr(func, '__annotations__', None):
                func.__annotations__ = dct = getattr(cls_func, '__annotations__', {}).copy()
                if dct.get('return') in {cls, cls.__name__}:
                    dct['return'] = sub_cls_name

            # Update docstring
            if func.__doc__ is None and cls_func.__doc__ is not None:
                doc_new = cls_func.__doc__.replace(cls.__name__, sub_cls_name)
                func.__doc__ = doc_new

            return func
        return decorator
