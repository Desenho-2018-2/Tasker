import logging
import json

from Orders.serializers import ObserverSerializer
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

    @abstractmethod
    def update(self):
        """
        Update a state of a observer
        """
        pass

class Target(AbstractTarget):
    """
    Base interface for target observer
    """

    def __init__(self):
        self.__observers = []

    def attach(self, observer):
        """
        Register a observer
        """

        if observer not in self.__observers:

            logging.debug("A observer was registered")

            self.__observers.append(observer)

            return True

        else:

            logging.debug("A observer has not been registered")

            return False

    def detach(self, observer):
        """
        Remove a observerd and return a boolean
        if the function has success
        """

        if observer in self.__observers:

            logging.debug("An observer was removed")

            self.remove(observer)

            return True

        else:

            logging.debug("The observer alredy has registered")

            return False

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
    pass

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
