"""A stub-only module containing a number of :class:`~typing.Protocol` subclasses."""

import sys
import types
from typing import (
    Tuple,
    TypeVar,
    Any,
    type_check_only
)

if sys.version_info >= (3, 8):
    from typing import Protocol, SupportsIndex as _SupportsIndex
else:
    from typing_extensions import Protocol

    @type_check_only
    class _SupportsIndex(Protocol):
        def __index__(self) -> int:
            pass

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)

@type_check_only
class _SupportsShape(Protocol):
    shape: Tuple[int, ...]

@type_check_only
class _SupportsCode(Protocol):
    __code__: types.CodeType

@type_check_only
class _SupportsAdd(Protocol[T_co]):
    def __add__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsSub(Protocol[T_co]):
    def __sub__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsMul(Protocol[T_co]):
    def __mul__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsFloordiv(Protocol[T_co]):
    def __floordiv__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsTruediv(Protocol[T_co]):
    def __truediv__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsPow(Protocol[T_co]):
    def __pow__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsMatmul(Protocol[T_co]):
    def __matmul__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsMod(Protocol[T_co]):
    def __mod__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsGt(Protocol[T_co]):
    def __gt__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsLt(Protocol[T_co]):
    def __lt__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsGe(Protocol[T_co]):
    def __ge__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsLe(Protocol[T_co]):
    def __le__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsNeg(Protocol[T_co]):
    def __neg__(self) -> T_co: ...

@type_check_only
class _SupportsPos(Protocol[T_co]):
    def __pos__(self) -> T_co: ...

@type_check_only
class _SupportsInvert(Protocol[T_co]):
    def __invert__(self) -> T_co: ...

@type_check_only
class _SupportsLshift(Protocol[T_co]):
    def __lshift__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsRshift(Protocol[T_co]):
    def __rshift__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsXor(Protocol[T_co]):
    def __xor__(self, x: Any) -> T_co: ...

@type_check_only
class _SupportsOr(Protocol[T_co]):
    def __or__(self, x: Any) -> T_co: ...
