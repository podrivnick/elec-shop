from dataclasses import dataclass

from django.db import transaction
from django.db.models import QuerySet

from core.apps.main.models.products import Products as ProductsModel
from core.apps.orders.entities.order import Order as OrderEntity
from core.apps.orders.exceptions.order import ExceptionNotEnoughQuantityProduct
from core.apps.orders.models.orders import Orders
from core.apps.orders.repositories.base import BaseCommandOrderRepository
from core.apps.orders.services.base import BaseCommandOrderService
from core.apps.users.models import User


@dataclass
class ORMBaseCommandOrderService(BaseCommandOrderService):
    command_create_orders_item_repository: BaseCommandOrderRepository

    def create_basic_order(
        self,
        user: QuerySet[User],
        order: OrderEntity,
    ) -> QuerySet[Orders]:
        basic_orders = Orders.objects.create(
            user=user,
            name_receiver=order.first_name.to_raw(),
            surname_receiver=order.last_name.to_raw(),
            phone_number=order.phone.to_raw(),
            required_delivery=order.required_delivery,
            delivery_address=order.delivery_address.to_raw(),
            has_paid=False,
            email=order.email.to_raw(),
            payment_on_get=order.payment_on_get,
            total_price=order.total_price.to_raw(),
        )

        return basic_orders

    def create_orders_items(
        self,
        basic_order: QuerySet[Orders],
        carts: QuerySet[ProductsModel],
    ) -> None:
        with transaction.atomic():
            for cart_item in carts:
                product = cart_item.product

                self.check_product_availability(product, cart_item.quantity)

                self.command_create_orders_item_repository.create_order_items(
                    order=self.basic_orders,
                    product=product,
                    name=product.name,
                    price=cart_item.products_price(),
                    quantity=cart_item.quantity,
                )

                product.count_product -= cart_item.quantity
                product.save()

        carts.delete()

    @staticmethod
    def check_product_availability(self, product, requested_quantity):
        if product.count_product < requested_quantity:
            raise ExceptionNotEnoughQuantityProduct(product.name)
