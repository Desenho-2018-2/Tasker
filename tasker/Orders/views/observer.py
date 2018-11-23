import logging
import json
import requests

from Orders.serializers import ObserverSerializer
from Orders.models.observer import Observer
from Orders.models.order import Order
from abc import ABC, abstractmethod
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class AbstractTarget(ABC):
    """
    Define a abstract with the methods for the target
    """

    @abstractmethod
    def notify(self):
        """
        Register a observer
        """
        pass

class AbstractObserver(ABC):
    """
    Define a abstract with the methods for the observer
    """

    @abstractmethod
    def update(self):
        """
        Update a state of a observer
        """
        pass

class OrderObserver(AbstractObserver):
    """
    Register a address for a POST method to be notified
    """

    def __init__(self, pk):
        """
        Create a observer class for the order pk
        """

        self.__model_pk = pk
        self.__observer = Observer.objects.get(pk=self.__model_pk)
    
    def update(self):

        # TODO Change test data to payload 
        post = requests.post(self.__observer.__str__,
                             data={'teste', 'teste'})
        
class Target(AbstractTarget):
    """
    Get a pk of a Order and notify all observer 
    the actual state of this Order
    """

    def __update_register(self, pk):
        """
        Query all oders
        """

        order_object = Order.objects.get(pk=pk)
        query = order_object.observer_set.all()

        logging.warn("Query of Target for pk: {} is {}".format(pk, query))

        return query

    def __init__(self, pk):
        
        # pk for Order model
        self.__observers_pk_key = pk

        # list with register observers
        self.__observers = self.__update_register(pk)

    def notify(self):
        """
        Notify all observers
        """

        logging.debug("Send message for all observers")

        for observer in self.__observers:
        
            OrderObserver(pk=observer.pk).update()

class OrderObserverView(APIView):
    """
    Represent a post method in another service
    """

    def get(self, request, format=None):

        query = Observer.objects.all()

        response = ObserverSerializer(query, many=True)

        return Response(response.data)

    def post(self, request, format=None):
        """
        Register a post method to another service
        """

        serializer = ObserverSerializer(data=request.data)

        if serializer.is_valid():
            logging.debug("A new observer was registered")

            observer_object = serializer.save()
            json_response = json.dumps({"observer_id": observer_object.id},
                                       separators=(':', ','))

            return Response(json_response)

        else:

            logging.debug("Someone try insert a observer in database")

            return Response(status=status.HTTP_400_BAD_REQUEST)
