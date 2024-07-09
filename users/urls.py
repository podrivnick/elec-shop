from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('change_below_profile/', views.change_below_profile, name='change_below_profile'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
]
