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

T_contra = TypeVar('T_contra', contravariant=True)
RT_co = TypeVar('RT_co', covariant=True)

@type_check_only
class _SupportsShape(Protocol):
    shape: Tuple[int, ...]

@type_check_only
class _SupportsCode(Protocol):
    __code__: types.CodeType

@type_check_only
class _SupportsNeg(Protocol[RT_co]):
    def __neg__(self) -> RT_co: ...

@type_check_only
class _SupportsPos(Protocol[RT_co]):
    def __pos__(self) -> RT_co: ...

@type_check_only
class _SupportsInvert(Protocol[RT_co]):
    def __invert__(self) -> RT_co: ...

@type_check_only
class _SupportsGetitem(Protocol[T_contra, RT_co]):
    def __getitem__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsAdd(Protocol[T_contra, RT_co]):
    def __add__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsSub(Protocol[T_contra, RT_co]):
    def __sub__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsMul(Protocol[T_contra, RT_co]):
    def __mul__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsFloordiv(Protocol[T_contra, RT_co]):
    def __floordiv__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsTruediv(Protocol[T_contra, RT_co]):
    def __truediv__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsPow(Protocol[T_contra, RT_co]):
    def __pow__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsMatmul(Protocol[T_contra, RT_co]):
    def __matmul__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsMod(Protocol[T_contra, RT_co]):
    def __mod__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsGt(Protocol[T_contra, RT_co]):
    def __gt__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsLt(Protocol[T_contra, RT_co]):
    def __lt__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsGe(Protocol[T_contra, RT_co]):
    def __ge__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsLe(Protocol[T_contra, RT_co]):
    def __le__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsLshift(Protocol[T_contra, RT_co]):
    def __lshift__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsRshift(Protocol[T_contra, RT_co]):
    def __rshift__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsXor(Protocol[T_contra, RT_co]):
    def __xor__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsOr(Protocol[T_contra, RT_co]):
    def __or__(self, x: T_contra) -> RT_co: ...

@type_check_only
class _SupportsEq(Protocol[RT_co]):
    def __eq__(self, x: Any) -> RT_co: ...  # type: ignore

@type_check_only
class _SupportsNe(Protocol[RT_co]):
    def __ne__(self, x: Any) -> RT_co: ...  # type: ignore
