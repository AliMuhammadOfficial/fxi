from django.urls import path
from .views import login_view, register_user, register_user_invited
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('register/<uuid:uid>', register_user_invited, name="invited"),
    path("logout/", LogoutView.as_view(), name="logout")
]