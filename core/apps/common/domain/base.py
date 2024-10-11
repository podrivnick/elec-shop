from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)


V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError()


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[V]):
    value: V

    def to_raw(self) -> V:
        return self.value


@dataclass(frozen=True, eq=False)
class Entity(ABC):
    pass


@dataclass(frozen=True, eq=False)
class ModelEntity(ABC):
    pass
