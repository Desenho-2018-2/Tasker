import json
import logging
import abc
import requests

from Orders import models
from Orders.models import Order, Observer
from Orders.serializers import OrdersSerializer
from Orders.views.observer import Observer
from django.http import Http404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# TODO create a factory to do this
def update_state(state, pk):

    map_handle = {models.WAITING_CONST : WaitState,
     models.COOKING_CONST : CookingState,
     models.DONE_CONST : DoneState,
     models.PICKIT_CONST : PickitState,
     models.CLOSE_CONST : CloseState,
     models.CANCEL_CONST : CancelState}

    handle_object = map_handle[state]

    return handle_object(pk).handle()

class State(metaclass=abc.ABCMeta):
    """
    Define an interface for encapsulating the behavior associated with a
    particular state of the Context.

    """
    def __init__(self, pk):
        self.__model_pk = pk

    @abc.abstractmethod
    def handle(self):
        pass

    def cancel(self):
        return models.CANCEL_CONST


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
    
        # target.notify(self.__model_pk)

    
        # target = Target.objects.filter(order=self.__model_pk)
    
        # for value in target:
           #  observer = Observer.objects.get(value.observer)
           #  post = requests.post(observer.__str__, data={"teste1":"teste2"})

        return models.PICKIT_CONST


class PickitState(State):
    def handle(self):
        return models.CLOSE_CONST

class CloseState(State):

    def handle(self):
        return models.CLOSE_CONST
