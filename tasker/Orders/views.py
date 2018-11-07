import logging

from Orders.serializers import OrdersSerializer
from Orders.models import Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class CRUDOrder(APIView):
    """
    This is the CRUD for Order models.
    """

    def post(self, request, format=None):
       
        order_serializer = OrdersSerializer(data=request.data)
        
        if orders_serializer.is_valid():
            logging.debug("The order is valid with the data {}".format(request.data))
            orders_serializer.save()

            return Response("Registrado")

        else:

            logging.debug("The order has failed with the data {}".format(request.data))
            return Response(orders_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):

        orders = Order.objects.all()
        orders_serialized = OrdersSerializer(orders, many=True)
        
        return Response(orders_serialized.data)

