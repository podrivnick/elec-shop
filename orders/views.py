from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.forms import ValidationError

from .forms import CreateOrder
from .models import OrderItem, Orders
from packet.models import Cart
from main_favorite.models import Products

data_form = {
    'first_name': 'first_name',
    'last_name': 'last_name',
    'email': 'email',
    'phone': 'phone',
}

def create_order(request):
    if request.method == 'POST':
        user = get_user_model().objects.get(username=request.user)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        delivery_address = request.POST.get('delivery_address')
        required_delivery = request.POST.get('required_delivery')
        payment_on_get = request.POST.get('payment_on_get')
        total_price = request.POST.get('total_price')

        try:
            orders = Orders.objects.create(
                user=user,
                name_receiver=first_name,
                surname_receiver=last_name,
                phone_number=phone,
                required_delivery=required_delivery,
                delivery_address=delivery_address,
                has_paid=False,
                email=email,
                payment_on_get=payment_on_get,
                total_price=total_price
            )

            packet = Cart.objects.filter(user=user)

            list_packet = [item for item in packet]

            for cart in list_packet:
                product = Products.objects.get(id_product=cart.product.id_product)

                if product.count_product < cart.quantity:
                    raise ValidationError(f'Недостаточное количество товара {product.name} на складе\
                                           В наличии - {product.count_product}')

                order_item = OrderItem.objects.create(
                    order=orders,
                    product=cart.product,
                    name=cart.product.name,
                    price=cart.products_price(),
                    quantity=cart.quantity
                )

                product.count_product -= cart.quantity

                product.save()

            packet.delete()

            messages.success(request, f"Заказ успешно оформлен")
            return redirect(reverse('main_favorite:index'))

        except ValidationError as e:
            orders.delete()
            messages.success(request, str(e))

            return redirect(reverse('carts_products:finalize_product'))
    else:
        return render(request, "carts_products/finalize_product.html")
