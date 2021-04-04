from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.plans, name="plans"),
    path('active', views.active, name="active")
]
