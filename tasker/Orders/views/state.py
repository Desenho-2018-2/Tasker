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
from abc import abstractmethod, ABCMeta

class AbstractTemplateOrderState(metaclass=ABCMeta):
    """
    Template algorithm for update a Order State
    """

    def __init__(self, pk):

        self.__order_pk = pk

    def get_order_model(self, pk):
        """
        Receive a pk and return a model django
        """

        return Order.objects.get(pk=pk)

    @abstractmethod
    def state_opeation(self, model_object):
        pass

    def save(self, order_object):
        """
        Receive a model order and save
        """

        order_object.save()

    def handle_state(self):
        """
        Base algorithm for state
        """

        model_object = self._get__order_model(self.__order_pk)
        new_model_object = self.state_operation(model_object)
        self.save(new_model_object)

class CancelTemplateState(AbstractTemplateOrderState):
    
    def state_operation(self, model_object):
        model_object.state = models.CANCEL_CONST

class WaitTemplateState(AbstractTemplateOrderState):
        
    def state_operation(self, model_object):
        model_object.state = models.COOKING_CONST

class CookingTemplateState(AbstractTemplateOrderState):
    
    def state_operation(self, model_object):
        model_object.state = models.DONE_CONST

class DoneTemplateState(AbstractTemplateOrderState):
    
    def state_operation(self, model_object):
       model_object.state = models.PICKIT_CONST

class CloseTemplateState(AbstractTemplateOrderState):
    
    def state_operation(self, model_object):
        model_object.state = model.CLOSE_CONST

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


class AbstractChain(metaclass=ABCMeta):

    @abstractmethod
    def handle(self, class_name):
        pass

class ConcreteChain(AbstractChain):
    """
    Redirect the responsability for a State class
    """

    def __init__(self, baseclass):
    
        # register all Factory classes 
         
        self.__map_handle = {
         models.WAITING_CONST : WaitState,
         models.COOKING_CONST : CookingState,
         models.DONE_CONST : DoneState,
         models.PICKIT_CONST : PickitState,
         models.CLOSE_CONST : CloseState,
         models.CANCEL_CONST : CancelState
        }

        # init the state class for handle the state
        self.__state = self.__init_state_class(baseclass)

    def __init_state_class(self, baseclass):
        """
        Handle the exception when you create a class
        """

        response = None

        try:
            response = self.__map_handle[baseclass]()
        except KeyError:
            logging.error("Someone try create a class not \
                          registered in Chain of Responsability")
            
        return response

    def handle(self, class_name):
        """ 
        Create a class registered in Chain
        """ 
    
        return self.__state.handle()


class AbstractFactory(metaclass=abc.ABCMeta):
    
    def __init__(self):
        self.__object = self.__fact

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
