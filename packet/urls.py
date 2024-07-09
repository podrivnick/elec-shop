from django.urls import path

from packet import views

app_name = "packet"

urlpatterns = [
    path('save_product_packet/', views.save_packet, name='save_product_packet'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('change_count_product/', views.change_count_product, name='change_count_product')
]
