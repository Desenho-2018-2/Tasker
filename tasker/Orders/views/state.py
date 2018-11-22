import logging
import abc

from Orders import models
from Orders.models import Order
from abc import abstractmethod, ABCMeta
from Orders.views.observer import Target

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
    def state_operation(self, model_object):
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

        model_object = self.get_order_model(self.__order_pk)
        new_model_object = self.state_operation(model_object)
        self.save(new_model_object)

class CancelTemplateState(AbstractTemplateOrderState):
    """
    Template for Cancel State
    """
    
    def state_operation(self, model_object):
        model_object.state = models.CANCEL_CONST

        return model_object

class WaitTemplateState(AbstractTemplateOrderState):
    """
    Template for Wait State
    """
        
    def state_operation(self, model_object):
        model_object.state = models.COOKING_CONST

        return model_object

class CookingTemplateState(AbstractTemplateOrderState):
    """
    Template for Cooking State
    """

    def state_operation(self, model_object):
        model_object.state = models.DONE_CONST

        return model_object

class DoneTemplateState(AbstractTemplateOrderState):
    """
    Template for Done State
    """
    
    def state_operation(self, model_object):
       model_object.state = models.PICKIT_CONST

       # Notify all observer 
       Target(model_object.pk).notify()

       return model_object

class PickitTemplateState(AbstractTemplateOrderState):
    """
    Template for PickIt State
    """

    def state_operation(self, model_object):
        model_object.state = models.CLOSE_CONST
        
        return model_object 

class CloseTemplateState(AbstractTemplateOrderState):
    """
    Template for Close State
    """
    
    def state_operation(self, model_object):
        model_object.state = models.CLOSE_CONST

        return model_object
