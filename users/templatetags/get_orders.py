from django import template
from django.contrib.auth import get_user_model

from orders.models import OrderItem


register = template.Library()


@register.simple_tag()
def get_orders(request):
    orders = OrderItem.objects.filter(order__user=request.user)
    list_orders = [item for item in orders]

    return list_orders