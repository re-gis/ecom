from django.contrib import admin
from django.urls import path

from orders import views

urlpatterns = [
    path("orders/", views.getOrders, name="orders"),
    path("create-order/", views.createOrder, name="create-order"),
]
