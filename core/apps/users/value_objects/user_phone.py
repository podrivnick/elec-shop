import re
from dataclasses import dataclass

from core.apps.common.domain.base import ValueObject
from core.apps.orders.utils.spec import IsStringSpec
from core.apps.orders.utils.validators import (
    IsNotEmptySpec,
    IsValidPhoneSpec,
    MaxLengthSpec,
)


MAX_PHONE_LENGTH = 32
PHONE_PATTERN = re.compile(r"^\+380\d{9}$")


@dataclass(frozen=True, eq=False)
class PhoneNumber(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        phone_spec = (
            IsStringSpec()
            .and_spec(IsNotEmptySpec())
            .and_spec(MaxLengthSpec(MAX_PHONE_LENGTH))
            .and_spec(IsValidPhoneSpec())
        )

        phone_spec.is_satisfied(self.value)

    def exists(self) -> bool:
        return self.value is not None
