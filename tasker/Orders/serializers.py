from rest_framework import serializers
from Orders.models import Order
from Orders.models import Observer

class OrdersSerializer(serializers.ModelSerializer):
    """
    Serializer class for Order model
    """

    class Meta:
        model = Order
        fields = '__all__'

class ObserverSerializer(serializers.ModelSerializer):
    """
    Serializer for the Observer model class
    """

    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = Observer
        fields = '__all__'
