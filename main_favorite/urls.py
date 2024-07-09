from django.urls import path

from main_favorite import views

app_name = "main_favorite"

urlpatterns = [
    path('', views.Main_Page.as_view(), name='index'),
    path('information/', views.info, name="information"),
    path('favorites/', views.favorites, name="favorites"),
    path('save_favorite', views.save_favorite, name="save_favorite"),
    path('<slug:category_slug>/', views.Main_Page.as_view(), name='category_equipped'),
]
