from django.urls import path

from carts_products import views


app_name = "carts_products"

urlpatterns = [
    path("save_opinion", views.SaveOpinion.as_view(), name="save_opinion"),
    path(
        "save_like_opinion/",
        views.ChangerCountLikeOpinion.as_view(),
        name="save_like_opinion",
    ),
    path("delete_opinion/", views.DeleteOpinion.as_view(), name="delete_opinion"),
    path("finalize_product/", views.Finalize.as_view(), name="finalize_product"),
    path("<slug:product>/", views.Product.as_view(), name="product"),
    path(
        "<slug:product>/opinions",
        views.OpinionsProduct.as_view(),
        name="product_all_opinion",
    ),
]
