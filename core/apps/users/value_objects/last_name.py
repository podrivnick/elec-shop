import re
from dataclasses import dataclass

from core.apps.common.domain.base import ValueObject
from core.apps.orders.utils.spec import IsStringSpec
from core.apps.orders.utils.validators import (
    IsAlphabeticSpec,
    IsNotEmptySpec,
    MaxLengthSpec,
)


MAX_LASTNAME_LENGTH = 50
LASTNAME_PATTERN = re.compile(r"^[A-Z][a-zA-Z'-]*$")


@dataclass(frozen=True, eq=False)
class LastName(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        last_name_spec = (
            IsStringSpec()
            .and_spec(IsNotEmptySpec())
            .and_spec(MaxLengthSpec(MAX_LASTNAME_LENGTH))
            .and_spec(IsAlphabeticSpec())
        )

        last_name_spec.is_satisfied(self.value)

    def exists(self) -> bool:
        return self.value is not None
