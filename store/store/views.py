from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, OrderSerializer

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getOrders(request):
    orders = 'orders.Order'.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createOrder(request):
    data = request.data
    order = 'orders.Order'.objects.create(
        customer=data['customer'],
        complete=data['complete'],
        transaction_id=data['transaction_id'],
    )
    order.save()
    return Response({'message': 'Order created successfully'})
