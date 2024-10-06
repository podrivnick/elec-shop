from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductEntity:
    id_product: str
    name: str
    description: str
    slug: str
    image: str
    discount: int
    price: int
    count_product: int
    category: str
    created_at: datetime
    updated_at: datetime

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price


@dataclass
class CategoriesProduct:
    category: str
    slug: str
