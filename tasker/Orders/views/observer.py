import logging
import json

from Orders.serializers import ObserverSerializer
from Orders.models.observer import Observer
from abc import ABC, abstractmethod
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class AbstractTarget(ABC):
    """
    Define a abstract with the methods for the target
    """

    @abstractmethod
    def attach(self):
        """
        Register a observer
        """
        pass

    @abstractmethod
    def detach(self):
        """
        Remove a observer
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notify all observer registered
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

class Target(AbstractTarget):
    """
    Get a pk of a Order and notify all observer 
    the actual state of this Order
    """

    def __update_register(self, pk):
        """
        Query all oders
        """

        query = Oders.objects.select_related('Observer').filter(pk=pk)

        return query

    def __init__(self, pk):
        
        # pk for Order model
        self.__observers_pk_key = pk

        # list with register observers
        self.__observer = self.__update_register(pk)

    def attach(self, observer):
        """
        Register a observer
        """

        verify_is_not_register = observer not in self.__observer

        if verify_is_not_register:

            logging.debug("A observer was registered")

            self.__observers.append(observer)

        else:

            logging.debug("A observer has not been registered")

        return verify_is_not_register

    def detach(self, observer):
        """
        Remove a observerd and return a boolean
        if the function has success
        """

        verify_is_register = observer in self.__observers

        if verify_is_register:

            logging.debug("An observer was removed")

            self.remove(observer)

        else:

            logging.debug("The observer alredy has registered")

        return verify_is_register


    def notify(self):
        """
        Notify all observers
        """

        logging.debug("Send message for all observers")

        for observer in self.__observers:
            observer.update()

class Observer(AbstractObserver):
    """
    Register a address for a POST method to be notified
    """

    def __init__(self, pk):
        """
        Create a observer class for the order pk
        """

        self.__model_pk = pk
    
    def update(self):
        observer = Observer.objects.get(pk=self.__model_pk)

        # TODO make this post the observer link
        post = requests.post(observr.__str__, data={'teste', 'teste'})
        
class OrderObserver(APIView):
    """
    Represent a post method in another service
    """

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

class OrderTarget(APIView):
    """
    Register, attach and detach observers
    """

    def __init__(self):
        self.__observers = []

    def notify(self):
        """
        Notify all observers
        """

        for observer in observers:
            observer.update()

    def post(self, observer):
        """
        Register a new observer
        """

        response_status = None

        if observer not in self.__observers:
            self.__observers.append(observer)
            response_status = status.HTTP_201_CREATE
        else:
            response_status = status=status.HTTP_400_BAD_REQUEST

        return Response(status=response_status)

    def delete(self, observer):
        """
        Remove a observer from the observer list
        """

        message = None
        code = None

        try:
            self.__observers.remove(observer)
            message = "Observer removed!"
            code = status.HTTP_200_OK

            logging.info("A observer as removed")

        except ValueError:

            message = "Observer don't exists"
            code = status.HTTP_400_BAD_REQUEST

            logging.warn("Someone try delete a observer not registered")

        return Response(message, status=code)
