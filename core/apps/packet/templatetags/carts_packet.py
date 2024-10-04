from django import template

from packet.utils import get_carts


register = template.Library()


@register.simple_tag()
def get_packets(request):
    return get_carts(request)
