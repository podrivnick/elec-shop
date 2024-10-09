from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    Optional,
    TypeVar,
)

from ninja import Schema


class PingResponseSchema(Schema):
    result: bool


TResult = TypeVar("TResult")
TException = TypeVar("TException")


@dataclass(frozen=True, eq=False)
class Response(Generic[TResult]):
    status: int


@dataclass(frozen=True, eq=False)
class SuccessResponse(Response[TResult]):
    status: int = field(default=200)
    result: Optional[TResult] = field(default=None)


@dataclass(frozen=True, eq=False)
class ErrorData(Generic[TException]):
    title: str = "Unknown error occurred"
    data: Optional[TException] | None = None


@dataclass(frozen=True, eq=False)
class FailureResponse(Response, Generic[TException]):
    status: int = 500
    error: ErrorData[TException] = field(default_factory=ErrorData)


@dataclass(frozen=True, eq=False)
class Template:
    template: str | None = field(default_factory="", kw_only=True)
