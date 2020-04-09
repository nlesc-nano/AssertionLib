"""Tests for the :mod:`AbstractDataClass<assertionlib.dataclass.AbstractDataClass>` class."""

import typing

from assertionlib import assertion
from assertionlib.dataclass import AbstractDataClass


def test_HASHABLE() -> None:
    """Tests for :meth:`AbstractDataClass._HASHABLE`."""
    class _TestClass1(AbstractDataClass):
        _HASHABLE = True

    class _TestClass2(AbstractDataClass):
        _HASHABLE = False

    obj1 = _TestClass1()
    obj2 = _TestClass2()
    assertion.assert_(hash, obj1)
    assertion.assert_(hash, obj2, exception=TypeError)


def test_init() -> None:
    """Tests for :meth:`AbstractDataClass.__init__`."""
    self = AbstractDataClass()

    assertion.eq(self._PRIVATE_ATTR, {'_PRIVATE_ATTR', '_hash'})
    assertion.eq(self._hash, 0)


def test_PRIVATE_ATTR() -> None:
    """Tests for :meth:`AbstractDataClass._PRIVATE_ATTR`."""
    cls = AbstractDataClass
    self = cls()

    assertion.isinstance(cls._PRIVATE_ATTR, frozenset)
    assertion.isinstance(self._PRIVATE_ATTR, set)
    assertion.eq(cls._PRIVATE_ATTR, frozenset())
    assertion.eq(self._PRIVATE_ATTR, {'_PRIVATE_ATTR', '_hash'})  # noqa


def test_repr() -> None:
    """Tests for :meth:`AbstractDataClass.__repr__`."""
    class TestClass(AbstractDataClass):
        def __init__(self, a, b, c):
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

    self = TestClass(1, 'bob', [1, 2, 3, 4, 5])
    ref1 = """TestClass(
    a = 1,
    b = 'bob',
    c = [1, 2, 3, 4, 5]
)"""
    assertion.str_eq(self, ref1)

    self.d = self  # type: ignore
    ref2 = f"""TestClass(
    a = 1,
    b = 'bob',
    c = [1, 2, 3, 4, 5],
    d = {object.__repr__(self).rstrip('>').rsplit(maxsplit=1)[1]}
)"""
    assertion.str_eq(self, ref2)


def test_eq() -> None:
    """Tests for :meth:`AbstractDataClass.__eq__`."""
    class TestClass1(AbstractDataClass):
        def __init__(self, a, b, c):
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

    class TestClass2(TestClass1):
        pass

    obj1 = TestClass1(1, 'bob', [1, 2, 3, 4, 5])
    obj2 = TestClass2(1, 'bob', [1, 2, 3, 4, 5])
    obj3 = TestClass1(1, 'bob', [1, 2, 3, 4, 5])

    assertion.eq(obj1, obj2, invert=True)
    assertion.eq(obj1, obj3)

    obj3.a = False
    assertion.eq(obj1, obj3, invert=True)

    obj1.a = obj1
    obj3.a = obj3
    assertion.eq(obj1, obj3, invert=True)


def test_hash() -> None:
    """Tests for :meth:`AbstractDataClass.__eq__`."""
    class TestClass(AbstractDataClass):
        def __init__(self, a, b, c):
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

    keys = ('a', 'b', 'c')

    obj1 = TestClass(1, 'bob', (1, 2, 3, 4, 5))
    ref1 = hash(TestClass)
    for k in keys:
        v = getattr(obj1, k)
        ref1 ^= hash((k, v))
    ref2 = ref1

    assertion.eq(obj1._hash, 0)
    assertion.eq(hash(obj1), ref1)
    assertion.eq(obj1._hash, ref1)
    assertion.eq(hash(obj1), ref1)

    obj2 = TestClass(1, 'bob', (1, 2, 3, 4, 5))
    assertion.eq(obj2._hash, 0)
    assertion.eq(hash(obj2), ref2)
    assertion.eq(obj2._hash, ref2)
    assertion.eq(hash(obj2), ref2)

    obj3 = TestClass(1, 'bob', (1, 2, 3, 4, 5))
    obj3.a = obj3
    ref3 = hash(type(obj3))
    ref3 ^= hash(('a', id(obj3)))
    for k in keys[1:]:
        v = getattr(obj3, k)
        ref3 ^= hash((k, v))
    assertion.eq(hash(obj3), ref3)

    obj4 = TestClass({1: 1}, {'a', 'b'}, [1, 2, 3, 4, 5])
    ref4 = hash(type(obj4))
    for k in keys:
        v = getattr(obj4, k)
        ref4 ^= hash((k, id(v)))
    assertion.eq(hash(obj4), ref4)


def test_copy() -> None:
    """Tests for :meth:`AbstractDataClass.copy`."""
    class TestClass(AbstractDataClass):
        def __init__(self, a, b, c):
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

    obj1 = TestClass({1: 1}, {1, 2, 3}, [1, 2, 3, 4, 5])
    obj2 = obj1.copy(deep=False)
    obj3 = obj1.copy(deep=True)

    assertion.eq(obj1, obj2)
    assertion.eq(obj1, obj3)

    attr_tup = ('a', 'b', 'c')
    for k in attr_tup:
        v1 = getattr(obj1, k)
        v2 = getattr(obj2, k)
        v3 = getattr(obj3, k)

        assertion.is_(v1, v2)
        assertion.is_not(v1, v3)


def test_as_dict() -> None:
    """Tests for :meth:`AbstractDataClass.as_dict`."""
    class TestClass(AbstractDataClass):
        def __init__(self, a, b, c):
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

    self = TestClass({1: 1}, {1, 2, 3}, [1, 2, 3, 4, 5])
    dct1 = self.as_dict()

    for k, v1 in dct1.items():
        v2 = getattr(self, k)
        assertion.eq(v1, v2)
        assertion.is_not(v1, v2)

    dct1 = self.as_dict(return_private=True)
    assertion.eq(dct1.keys(), vars(self).keys())


def test_from_dict() -> None:
    """Tests for :meth:`AbstractDataClass.from_dict`."""
    class TestClass(AbstractDataClass):
        def __init__(self, a, b, c):
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

    obj1 = TestClass({1: 1}, {1, 2, 3}, [1, 2, 3, 4, 5])
    dct = {'a': {1: 1}, 'b': {1, 2, 3}, 'c': [1, 2, 3, 4, 5]}
    obj2 = TestClass.from_dict(dct)

    assertion.eq(obj1, obj2)


class _TestClass(AbstractDataClass):
    @AbstractDataClass.inherit_annotations()
    def _str_iterator(self):
        iterable = super()._str_iterator()
        return sorted((k.strip('_'), v) for k, v in iterable)


def test_inherit_annotations() -> None:
    """Tests for :meth:`AbstractDataClass.inherit_annotations`."""
    ref1 = 'Return an iterable for the :meth:`_TestClass.__repr__` method.'
    ref2 = {'return': typing.Iterable[typing.Tuple[str, typing.Any]]}
    func = _TestClass._str_iterator

    assertion.eq(func.__doc__, ref1)
    assertion.eq(func.__annotations__, ref2)
