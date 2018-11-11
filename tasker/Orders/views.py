import json
import logging
import abc

from Orders import models
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

        order_object = get_order(pk)

        order_object.state = CancelState().handle()

        order_object.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        """
        Update a order in database
        """

        pk = request.data['order_id']

        order_object = get_order(pk)

        order_object.state = update_state(order_object.state)

        order_object.save()

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

# TODO create a factory to do this
def update_state(state):
    
    map_handle = {models.WAITING_CONST : WaitState,
     models.COOKING_CONST : CookingState,
     models.DONE_CONST : DoneState,
     models.PICKIT_CONST : PickitState,
     models.CLOSE_CONST : CloseState,
     models.CANCEL_CONST : CancelState}

    handle_object = map_handle[state]
    
    return handle_object().handle()

class State(metaclass=abc.ABCMeta):
    """
    Define an interface for encapsulating the behavior associated with a
    particular state of the Context.
    """

    @abc.abstractmethod
    def handle(self):
        pass

    def cancel(self):
        return 'ERROR'


class CancelState(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def handle(self):
        return models.CANCEL_CONST

class WaitState(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def handle(self):
        return models.COOKING_CONST

class CookingState(State):  
    def handle(self):
        return models.DONE_CONST

class DoneState(State):
    def handle(self):
        return models.PICKIT_CONST

class PickitState(State):
    def handle(self):
        return models.CLOSE_CONST 

class CloseState(State):

    def handle(self):
        return models.CLOSE_CONST

