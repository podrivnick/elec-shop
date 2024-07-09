from django.urls import path

from carts_products import views

app_name = "carts_products"

urlpatterns = [
    path('save_opinion', views.save_opinion, name='save_opinion'),
    path('save_like_opinion/', views.save_like_opinion, name='save_like_opinion'),
    path('delete_opinion/', views.delete_opinion, name='delete_opinion'),
    path('finalize_product/', views.Finalize.as_view(), name='finalize_product'),
    path('<slug:product>/', views.Product.as_view(), name='product'),
    path('<slug:product>/opinions', views.OpinionsProduct.as_view(), name='product_all_opinion'),
]
