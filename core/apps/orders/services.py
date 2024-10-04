from core.apps.main.models.products import Products

from .exceptions import ExceptionNotEnoughQuantityProduct
from .models import OrderItem


# from packet.models import Cart


class CreateBasicOrders:
    def __init__(self, *args):
        self.user = args[0]
        self.basic_orders = args[1]

    def create_order(self):
        packet = Cart.objects.filter(user=self.user).order_by("quantity")  # noqa

        list_packet = [item for item in packet]  # noqa

        for cart in list_packet:
            product = Products.objects.get(id_product=cart.product.id_product)

            if product.count_product < cart.quantity:
                raise ExceptionNotEnoughQuantityProduct(product.name)

            OrderItem.objects.create(
                order=self.basic_orders,
                product=cart.product,
                name=cart.product.name,
                price=cart.products_price(),
                quantity=cart.quantity,
            )

            product.count_product -= cart.quantity

            product.save()

        packet.delete()
