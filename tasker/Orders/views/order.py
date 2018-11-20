import json
import logging

from Orders.views.chain import UpdateChain, HandleRequestStateChain
from Orders.models import Order
from Orders.serializers import OrdersSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class CRUDOrder(APIView):
    """
    This is the CRUD for Order models.
    """

    def post(self, request, format=None):
        """
        Insert a order in a database
        """

        orders_serializer = OrdersSerializer(data=request.data)

        if orders_serializer.is_valid():
            logging.debug("The order is valid with the data {}"\
                          .format(request.data))

            order_object = orders_serializer.save()

            json_response = json.dumps({"order_id":order_object.id},
                                       separators=(':', ','))

            return Response(json_response)

        else:

            logging.debug("The order has failed with the data {}" \
                          .format(request.data))

            return Response(orders_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """
        Get all orders in database
        """

        orders = return_queue()
        orders_serialized = OrdersSerializer(orders, many=True)

        return Response(orders_serialized.data)

    def delete(self, request, format=None):
        """
        Delete a order in the database
        """

        pk = request.data['delete_order_id']

        HandleRequestStateChain().handle_request('CANCEL', pk)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        """
        Update a order in database
        """

        pk = request.data['order_id']

        UpdateChain().handle_request(pk=pk)

        logging.debug("Order {} updated".format(pk))
        return Response("Order with id {} update successful!".format(pk))


def get_order(pk):
    """
    Return a order from the database
    """

    Order.objects.get(pk=pk)

    try:
        return Order.objects.get(pk=pk)
    except:
        raise Http404

def return_queue():

    orders = Order.objects.filter(order_type="FOOD").order_by('state', 'time', 'table', 'date')

    return orders
