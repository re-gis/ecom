from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import OrderSerializer
from rest_framework.response import Response


# Create your views here.
@api_view(["GET"])
def getOrders(request):
    orders = "orders.Order".objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def createOrder(request):
    data = request.data
    order = "orders.Order".objects.create(
        customer=data["customer"],
        complete=data["complete"],
        transaction_id=data["transaction_id"],
    )
    order.save()
    return Response({"message": "Order created successfully"})
