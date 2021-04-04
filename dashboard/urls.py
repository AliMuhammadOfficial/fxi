from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('admin/', views.admin, name="admin"),
    path('admin/<str:page>/', views.page, name="page"),
    path('deposit/', views.deposit, name="deposit"),
    path('withdrawal/', views.withdrawal, name="withdrawal"),
]
