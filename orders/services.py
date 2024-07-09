from django.core.exceptions import ValidationError
from main_favorite.models import Products
from packet.models import Cart

from .config import NOT_ENOUGH_COUNT_PRODUCTS
from .models import OrderItem


class CreateBasicOrders:

    def __init__(self, *args):
        self.user = args[0]
        self.basic_orders = args[1]

    def create_basic_orders(self):

        packet = Cart.objects.filter(user=self.user)

        list_packet = [item for item in packet]

        for cart in list_packet:
            product = Products.objects.get(id_product=cart.product.id_product)

            if product.count_product < cart.quantity:
                raise ValidationError(f"{NOT_ENOUGH_COUNT_PRODUCTS}{product.name}")

            order_item = OrderItem.objects.create(
                order=self.basic_orders,
                product=cart.product,
                name=cart.product.name,
                price=cart.products_price(),
                quantity=cart.quantity
            )

            product.count_product -= cart.quantity

            product.save()

        packet.delete()
