from django.urls import path

from main_favorite import views


app_name = "main_favorite"

urlpatterns = [
    path("", views.MainPage.as_view(), name="index"),
    path("information/", views.BaseInformation.as_view(), name="information"),
    path("favorites/", views.FavoritesPage.as_view(), name="favorites"),
    path("save_favorite", views.SaveFavorite.as_view(), name="save_favorite"),
    path("<slug:category_slug>/", views.MainPage.as_view(), name="category_equipped"),
]
