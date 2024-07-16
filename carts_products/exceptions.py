from dataclasses import dataclass

from orders.config import MISTAKE_BASE_CLASS_EXCEPTION


@dataclass
class BaseExceptionClass(Exception):
    @property
    def message(self):
        return f"{MISTAKE_BASE_CLASS_EXCEPTION}"


@dataclass
class AttributeNotInObject(BaseExceptionClass):
    attribute: str
    object_name: str

    @property
    def message(self):
        return f"Attribute {self.attribute} not in {self.object_name}"


@dataclass
class ObjectNotValid(BaseExceptionClass):
    object_name: str

    @property
    def message(self):
        return f"Object {self.object_name} not valid object"


@dataclass
class AttributeNotValid(BaseExceptionClass):
    object_name: str
    value: str

    @property
    def message(self):
        return f"Attribute {self.value} not valid for {self.object_name}"
