from django.http import HttpRequest

from core.api.v1.orders.dto.base import DTOCreateOrderAPI


def extract_create_order_dto(
    request: HttpRequest,
) -> DTOCreateOrderAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    delivery_address = request.POST.get("delivery_address")
    required_delivery = request.POST.get("required_delivery")
    payment_on_get = request.POST.get("payment_on_get")
    total_price = request.POST.get("total_price")

    return DTOCreateOrderAPI(
        is_authenticated=is_authenticated,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        delivery_address=delivery_address,
        required_delivery=required_delivery,
        payment_on_get=payment_on_get,
        total_price=total_price,
    )
