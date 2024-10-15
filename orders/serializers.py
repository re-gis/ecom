from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = "orders.Order"
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = "orders.OrderItem"
        fields = "__all__"
