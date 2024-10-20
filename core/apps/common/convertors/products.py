from django.db.models import QuerySet

from core.apps.main.entities.product import ProductEntity
from core.apps.main.models.products import Products


def convert_product_entity_to_model(
    product: ProductEntity,
) -> QuerySet[Products]:
    return Products(
        **product.to_dict(),
    )
