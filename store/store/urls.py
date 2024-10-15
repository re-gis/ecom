from django.urls import path
from .views import getProducts, getProduct, createProduct, updateProduct, deleteProduct

urlpatterns = [
    path("", getProducts, name="get_products"),
    path("/<int:pk>", getProduct, name="get_product"),
    path("/create", createProduct, name="create_product"),
    path("/update/<int:pk>", updateProduct, name="update_product"),
    path("/delete/<int:pk>", deleteProduct, name="delete_product"),
]
