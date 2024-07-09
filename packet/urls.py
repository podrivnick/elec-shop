from django.urls import path

from packet import views

app_name = "packet"

urlpatterns = [
    path('save_product_packet/', views.AddProductToPacket.as_view(), name='save_product_packet'),
    path('delete_cart/', views.DeleteCartFromPacket.as_view(), name='delete_cart'),
    path('change_count_product/', views.ChangeCountProductPacket.as_view(), name='change_count_product')
]
