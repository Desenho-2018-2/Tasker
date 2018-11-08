from rest_framework import serializers
from Orders.models import Order

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


