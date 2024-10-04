from django import template

from orders.models import OrderItem


register = template.Library()


@register.simple_tag()
def get_orders(request):
    orders = OrderItem.objects.filter(order__user=request.user)
    list_orders = [item for item in orders]  # noqa

    return list_orders
