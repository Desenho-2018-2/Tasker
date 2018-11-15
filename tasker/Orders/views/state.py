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
