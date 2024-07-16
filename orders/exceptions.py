from dataclasses import dataclass

from .config import MISTAKE_BASE_CLASS_EXCEPTION, NOT_ENOUGH_COUNT_PRODUCTS


@dataclass
class BaseOrderException(Exception):
    @property
    def exception(self):
        return f'{MISTAKE_BASE_CLASS_EXCEPTION}'


@dataclass
class ExceptionNotEnoughQuantityProduct(BaseOrderException):
    name_product: str

    @property
    def exception(self):
        return f"{NOT_ENOUGH_COUNT_PRODUCTS}{self.name_product}"

