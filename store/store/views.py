from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def getProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProduct(request):
    if request.user.role is not "ADMIN":
        return Response(
            {"error": "You are not authorized to create a product."},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProduct(request, pk):
    if request.user.role is not "ADMIN":
        return Response(
            {"error": "You are not authorized to update a product."},
            status=status.HTTP_403_FORBIDDEN,
        )
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(instance=product, data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteProduct(request, pk):
    if request.user.role is not "ADMIN":
        return Response(
            {"error": "You are not authorized to delete a product."},
            status=status.HTTP_403_FORBIDDEN,
        )
    try:
        with transaction.atomic():
            product = Product.objects.get(id=pk)
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )
