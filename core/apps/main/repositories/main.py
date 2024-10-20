from dataclasses import dataclass
from typing import Optional

from django.db.models import QuerySet

from core.apps.main.models.products import Products
from core.apps.main.repositories.base import BaseQueryProductRepository


@dataclass
class ORMQueryProductRepository(BaseQueryProductRepository):
    def filter_product_by_slug(
        self,
        slug: Optional[str],
    ) -> QuerySet[Products]:
        product = Products.objects.filter(slug=slug)

        return product
