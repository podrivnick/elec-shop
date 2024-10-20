from dataclasses import dataclass
from datetime import datetime
from typing import (
    Dict,
    Optional,
)


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
    headline: Optional[str] = ""
    bodyline: Optional[str] = ""

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

    def to_dict(self) -> Dict:
        return {
            "id_product": self.id_product,
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "image": self.image,
            "discount": self.discount,
            "price": self.price,
            "count_product": self.count_product,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class CategoriesProduct:
    category: str
    slug: str
