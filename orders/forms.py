from django import forms

from .models import Orders

class CreateOrder(forms.Form):
    class Meta:
        model = Orders
        fields = ['first_name', 'last_name', 'email',
                  'phone', 'delivery_address', 'required_delivery',
                  'payment_on_get']

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    delivery_address = forms.CharField(required=False)
    required_delivery = forms.BooleanField(initial=False)
    payment_on_get = forms.BooleanField(initial=True)
