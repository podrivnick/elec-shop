from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('registration/', views.RegisterUser.as_view(), name='registration'),
    path('change_below_profile/', views.ChangeDataBelowProfile.as_view(), name='change_below_profile'),
    path('profile/', views.ProfileUserData.as_view(), name='profile'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
