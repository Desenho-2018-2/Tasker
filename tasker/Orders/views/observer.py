import logging

from rest_framework import status
from rest_framework.response import Response

class OrderTarget:
    pass


class OrderObserver:
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

    def attach(self, observer):
        """
        Register a new observer
        """
    
        if observer not in self.__observers:
            self.__observers.append(observer)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

            logging.warn("Someone try delete a observer not registered")

            message = "Observer don't exists"
            code = status.HTTP_400_BAD_REQUEST

        return Response(message, status=code)
