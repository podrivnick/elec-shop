import logging
from dataclasses import dataclass
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from core.apps.main.models.products import Products as ProductsModel
from core.apps.orders import value_objects as vo_orders
from core.apps.orders.entities.order import Order as OrderEntity
from core.apps.orders.exceptions.order import ExceptionNotEnoughQuantityProduct
from core.apps.orders.models.orders import Orders
from core.apps.orders.repositories.base import BaseCommandOrderRepository
from core.apps.orders.services.base import (
    BaseCommandOrderService,
    BaseQueryValidationOrderService,
)
from core.apps.users import value_objects as vo
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

                self.check_product_availability(
                    product=product,
                    requested_quantity=cart_item.quantity,
                )

                self.command_create_orders_item_repository.create_order_items(
                    order=basic_order,
                    product=product,
                    name=product.name,
                    price=self.products_price(cart_item=cart_item, product=product),
                    quantity=cart_item.quantity,
                )

                product.count_product -= cart_item.quantity
                product.save()

        carts.delete()

    @staticmethod
    def products_price(cart_item, product) -> int:
        price = product.price
        if product.discount:
            price = round(product.price - product.price * product.discount / 100, 2)

        return round(price * cart_item.quantity, 2)

    @staticmethod
    def check_product_availability(product, requested_quantity):
        if product.count_product < requested_quantity:
            raise ExceptionNotEnoughQuantityProduct(product.name)


@dataclass
class QueryValidationOrderService(BaseQueryValidationOrderService):
    def validate_order_data(
        self,
        first_name: Optional[str],
        last_name: Optional[str],
        email: Optional[str],
        phone: Optional[str],
        delivery_address: Optional[str],
        required_delivery: Optional[str],
        payment_on_get: Optional[str],
        total_price: Optional[str],
    ) -> OrderEntity:
        logging.info(total_price)
        first_name = vo.FirstName(first_name)
        last_name = vo.LastName(last_name)
        email = vo.Email(email)
        phone = vo.PhoneNumber(phone)
        delivery_address = vo_orders.DeliveryAddress(delivery_address)
        total_price = vo_orders.TotalPrice(total_price)

        return OrderEntity.create_order_entity(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            delivery_address=delivery_address,
            required_delivery=required_delivery,
            payment_on_get=payment_on_get,
            total_price=total_price,
        )
