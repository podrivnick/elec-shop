from django import template

from core.apps.orders.models.orders import OrderItem


register = template.Library()


@register.simple_tag()
def get_orders(request):
    orders = OrderItem.objects.filter(order__user=request.user)
    list_orders = list(orders)

    return list_orders
