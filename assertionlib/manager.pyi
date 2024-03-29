"""Stub files for :mode:`assertionlib.manager`."""

import os
import sys
import types
import reprlib
import inspect
from typing import (
    Any,
    Hashable,
    AbstractSet,
    Callable,
    FrozenSet,
    Type,
    TypeVar,
    Tuple,
    Sized,
    SupportsFloat,
    SupportsInt,
    SupportsAbs,
    SupportsRound,
    Sequence,
    Mapping,
    Container,
    Iterable,
    NoReturn,
    type_check_only,
    overload
)

import numpy as np

from .dataclass import AbstractDataClass, _MetaADC
from .protocol import (
    _SupportsIndex,
    _SupportsShape,
    _SupportsCode,
    _SupportsAdd,
    _SupportsSub,
    _SupportsMul,
    _SupportsFloordiv,
    _SupportsTruediv,
    _SupportsPow,
    _SupportsMatmul,
    _SupportsMod,
    _SupportsGt,
    _SupportsLt,
    _SupportsGe,
    _SupportsLe,
    _SupportsNeg,
    _SupportsInvert,
    _SupportsRshift,
    _SupportsLshift,
    _SupportsPos,
    _SupportsXor,
    _SupportsOr,
    _SupportsGetitem,
    _SupportsEq,
    _SupportsNe,
    _SupportsAnd,
    _SupportsLengthHint
)

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
RT = TypeVar('RT')

@type_check_only
class _MetaAM(_MetaADC):
    EXCLUDE: FrozenSet[str] = ...
    INCLUDE: FrozenSet[Callable[..., Any]] = ...

class AssertionManager(AbstractDataClass, metaclass=_MetaAM):
    repr_instance: reprlib.Repr | None
    repr_fallback: Callable[[object], str]
    maxstring_fallback: int

    def __init__(self, repr_instance: reprlib.Repr | None = ...) -> None: ...
    @property
    def repr(self) -> Callable[[object], str]: ...
    @property
    def maxstring(self) -> int: ...

    @overload
    def assert_(self, __func: Callable[..., Any], *args: Any, exception: None = ..., invert: bool = ..., post_process: None = ..., message: str | None = ..., **kwargs: Any) -> None: ...
    @overload
    def assert_(self, __func: Callable[..., RT], *args: Any, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object], message: str | None = ..., **kwargs: Any) -> None: ...
    @overload
    def assert_(self, __func: Callable[..., Any], *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...
    def __call__(self, __value: RT, *, invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    def add_to_instance(self, func: Callable[..., Any], name: str | None = ..., override_attr: bool = ...) -> None: ...

    # operators

    @overload
    def abs(self, __a: SupportsAbs[RT], *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def abs(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def add(self, __a: _SupportsAdd[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def add(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def and_(self, __a: _SupportsAnd[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def and_(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def concat(self, __a: Sequence[T1], __b: Sequence[T2], *, exception: None = ..., invert: bool = ..., post_process: Callable[[Sequence[T1 | T2]], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def concat(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def contains(self, __a: Container[Any], __b: Any, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def contains(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def countOf(self, __a: Iterable[Any], __b: Any, *, exception: None = ..., invert: bool = ..., post_process: Callable[[int], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def countOf(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    # .ne() and .eq() need an extra overload for __a = None as NoneType.__eq__() is not annotated

    @overload
    def eq(self, __a: _SupportsEq[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def eq(self, __a: None, __b: Any, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def eq(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def floordiv(self, __a: _SupportsFloordiv[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def floordiv(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def ge(self, __a: _SupportsGe[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def ge(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def getitem(self, __a: _SupportsGetitem[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def getitem(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def gt(self, __a: _SupportsGt[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def gt(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def index(self, __a: _SupportsIndex, *, exception: None = ..., invert: bool = ..., post_process: Callable[[int], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def index(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def indexOf(self, __a: Iterable[Any], __b: Any, *, exception: None = ..., invert: bool = ..., post_process: Callable[[int], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def indexOf(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def inv(self, __a: _SupportsInvert[RT], *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def inv(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def invert(self, __a: _SupportsInvert[RT], *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def invert(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def is_(self, __a: object, __b: object, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def is_(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def is_not(self, __a: object, __b: object, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def is_not(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def le(self, __a: _SupportsLe[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def le(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def lshift(self, __a: _SupportsLshift[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def lshift(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def lt(self, __a: _SupportsLt[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def lt(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def matmul(self, __a: _SupportsMatmul[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def matmul(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def mod(self, __a: _SupportsMod[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def mod(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def mul(self, __a: _SupportsMul[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def mul(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    # .ne() and .eq() need an extra overload for __a = None as NoneType.__eq__() is not annotated

    @overload
    def ne(self, __a: _SupportsNe[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def ne(self, __a: None, __b: Any, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def ne(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def neg(self, __a: _SupportsNeg[RT], *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def neg(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def not_(self, __a: object, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def not_(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def or_(self, __a: _SupportsOr[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def or_(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def pos(self, __a: _SupportsPos[RT], *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def pos(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def pow(self, __a: _SupportsPow[int, RT], __b: int, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def pow(self, __a: _SupportsPow[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def pow(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def rshift(self, __a: _SupportsRshift[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def rshift(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def sub(self, __a: _SupportsSub[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def sub(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def truediv(self, __a: _SupportsTruediv[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def truediv(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def truth(self, __a: object, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def truth(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def xor(self, __a: _SupportsXor[T, RT], __b: T, *, exception: None = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def xor(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def length_hint(self, __obj: Sized | _SupportsLengthHint, *, default: int = ..., invert: bool = ..., post_process: Callable[[int], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def length_hint(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    # builtins

    @overload
    def callable(self, __obj: Any, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def callable(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isinstance(self, __obj: Any, __class_or_tuple: type | Tuple[type, ...], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isinstance(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def issubclass(self, __cls: type, __class_or_tuple: type | Tuple[type, ...], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def issubclass(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def hasattr(self, __obj: Any, __name: str, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def hasattr(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def len(self, __obj: Sized, *, exception: None = ..., invert: bool = ..., post_process: Callable[[int], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def len(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def any(self, __obj: Iterable[None | object], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def any(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def all(self, __obj: Iterable[None | object], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def all(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isdisjoint(self, __a: Iterable[Hashable], __b: Iterable[Hashable], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isdisjoint(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def issuperset(self, __a: Iterable[Hashable], __b: Iterable[Hashable], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def issuperset(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def issubset(self, __a: Iterable[Hashable], __b: Iterable[Hashable], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def issubset(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def round(self, __number: SupportsRound[RT], *, ndigits: int = ..., invert: bool = ..., post_process: Callable[[RT], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def round(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    # os

    @overload
    def isabs(self, __s: str | bytes | os.PathLike[Any], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isabs(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def islink(self, __path: str | bytes | os.PathLike[Any], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def islink(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def ismount(self, __path: str | bytes | os.PathLike[Any], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def ismount(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isdir(self, __s: str | bytes | os.PathLike[Any], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isdir(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isfile(self, __path: str | bytes | os.PathLike[Any], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isfile(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    # math

    @overload
    def isinf(self, __x: SupportsFloat, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isinf(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isnan(self, __x: SupportsFloat, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isnan(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isfinite(self, __x: SupportsFloat, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isfinite(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def isclose(self, __a: SupportsFloat, __b: SupportsFloat, *, rel_tol: SupportsFloat = ..., abs_tol: SupportsFloat = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def isclose(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def allclose(self, __a: SupportsFloat, __b: SupportsFloat, *, rel_tol: SupportsFloat = ..., abs_tol: SupportsFloat = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def allclose(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    # misc

    @overload
    def shape_eq(self, __a: _SupportsShape, __b: _SupportsShape | Tuple[SupportsInt, ...], *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def shape_eq(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def len_eq(self, __a: Sized, __b: SupportsInt, *, exception: None = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def len_eq(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

    @overload
    def str_eq(self, __a: T, __b: str, *, str_converter: Callable[[T], str] = ..., invert: bool = ..., post_process: Callable[[bool], object] | None = ..., message: str | None = ...) -> None: ...
    @overload
    def str_eq(self, *args: Any, exception: Type[Exception], invert: bool = ..., post_process: Callable[[Any], Any] | None = ..., message: str | None = ..., **kwargs: Any) -> None: ...

assertion: Final[AssertionManager] = ...
