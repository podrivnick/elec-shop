from typing import List

from django import template

from core.apps.main.entities.product import ProductEntity
from core.apps.orders.models.orders import OrderItem
from core.apps.orders.schemas.main import OrderItemSchema


register = template.Library()


@register.simple_tag()
def get_orders(request) -> List[OrderItemSchema]:
    orders = OrderItem.objects.filter(order__user=request.user)
    list(orders)

    list_orders_entities = [create_order_item_entity(item) for item in orders]

    return list_orders_entities


def create_order_item_entity(item) -> OrderItemSchema:
    """Создаем сущность элементов заказа на основе модели OrderItem."""
    return OrderItemSchema(
        pk=item.pk,
        order=item.order if item.order else None,
        name=item.name,
        product=ProductEntity(
            id_product=item.product.id_product,
            name=item.product.name,
            description=item.product.description,
            slug=item.product.slug,
            image=item.product.image,
            discount=item.product.discount,
            price=item.product.price,
            count_product=item.product.count_product,
            category=item.product.category,
            created_at=item.product.created_at,
            updated_at=item.product.updated_at,
        ),
        quantity=item.quantity,
        price=item.price,
        created_timestamp=item.created_timestamp,
    )
