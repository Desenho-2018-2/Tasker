import logging

from abc import abstractmethod, ABCMeta
from Orders import models
from Orders.models import Order
from Orders.views.state import CancelTemplateState
from Orders.views.state import WaitTemplateState
from Orders.views.state import CookingTemplateState
from Orders.views.state import DoneTemplateState
from Orders.views.state import PickitTemplateState
from Orders.views.state import CloseTemplateState

class AbstractChain(metaclass=ABCMeta):
    """
    Abstract Chain class
    """

    @abstractmethod
    def handle_request(self, request_name, pk):
        pass


class HandleRequestStateChain(AbstractChain):
    """
    Chain of responsability for Cancel and Update State
    """

    def handle_request(self, request_name, pk):
    
        if request_name=='CANCEL':
                    
            CancelTemplateState(pk=pk).handle_state()
                    
        elif request_name=='UPDATE':

            UpdateChain().handle_request(pk=pk)

        else:

            logging.error("A request does not have a valid state")
            raise Exception('NOT A VALID STATE')
        

class UpdateChain(AbstractChain):
    """
    Redirect the responsability for a State class
    """

    def __init__(self):
    
        # register all Factory classes 
         
        self.__map_handle = {
         models.WAITING_CONST : WaitTemplateState,
         models.COOKING_CONST : CookingTemplateState,
         models.DONE_CONST : DoneTemplateState,
         models.PICKIT_CONST : PickitTemplateState,
         models.CLOSE_CONST : CloseTemplateState
        }

    def handle_request(self, class_name=None, pk=None):
        """ 
        Create a class registered in Chain
        """ 

        if pk:

            model_state = Order.objects.get(pk=pk).state
            
            self.__map_handle[model_state](pk=pk).handle_state()

            logging.info("The state of {} has updated".format(pk))
            
        else:
            # TODO handle this exception

            logging.error("PK not inserted in handle_request UpdateChain")
            raise Exception("PK in chain not inserted")
