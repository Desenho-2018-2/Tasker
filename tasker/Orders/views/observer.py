import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class OrderObserver(APIView):
    """
    Represent a post method in another service 
    """

    def post(self, request):
        """
        Register a post method to another service
        """

        pass

class OrderTarget(APIView):
    """
    Register, attach and detach observers
    """

    class Meta:
        abstract = True

    def __init__(self):
        self.__observers = []

    def notify(self):
        """
        Notify all observers
        """
        
        for observer in observers:
            observer.update()

    def attach(self, observer):
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

    def detach(self, observer):
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
