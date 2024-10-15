# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    customer = request.user.customer 
    cart, created = Cart.objects.get_or_create(customer=customer)

    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product_id=product_id
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    customer = request.user.customer
    cart = get_object_or_404(Cart, customer=customer)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    customer = request.user.customer
    cart = get_object_or_404(Cart, customer=customer)

    cart.items.all().delete() 
    cart.delete()  
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    customer = request.user.customer
    cart = get_object_or_404(Cart, customer=customer)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_cart_item_quantity(request, item_id):
    customer = request.user.customer
    cart = get_object_or_404(Cart, customer=customer)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    quantity = request.data.get("quantity")
    if quantity is not None and quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    return Response({"detail": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
