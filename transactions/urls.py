from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.transactions, name="transactions"),
    path('edit/<int:trx_id>', views.edit_transaction, name="edittransaction")
]
