import re
from dataclasses import dataclass

from core.apps.common.domain.base import ValueObject
from core.apps.orders.utils.spec import IsStringSpec
from core.apps.orders.utils.validators import (
    IsAlphabeticSpec,
    IsNotEmptySpec,
    MaxLengthSpec,
    NoSpecialCharactersSpec,
)


MAX_ADDRESS_LENGTH = 120
ADDRESS_PATTERN = re.compile(r"^[A-Z][a-zA-Z'-]*$")


@dataclass(frozen=True, eq=False)
class DeliveryAddress(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        delivery_address_spec = (
            IsStringSpec()
            .and_spec(IsNotEmptySpec())
            .and_spec(MaxLengthSpec(MAX_ADDRESS_LENGTH))
            .and_spec(IsAlphabeticSpec())
            .and_spec(NoSpecialCharactersSpec())
        )

        delivery_address_spec.is_satisfied(self.value)

    def exists(self) -> bool:
        return self.value is not None
