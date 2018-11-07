from rest_framework import serializers
from Orders.models import Orders

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'date_time')


