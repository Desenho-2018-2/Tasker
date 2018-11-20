from abc import abstractmethod, ABCMeta
from Orders.views import CancelTemplateState

class AbstractChain(metaclass=ABCMeta):
    """
    Abstract Chain class
    """

    @abstractmethod
    def handle_request(self, request_name):
        pass


class HandleRequestStateChain(AbstractChain):
    """
    Chain of responsability for Cancel and Update State
    """

    def handle_request(self, request_name, pk):
    
        if request_name=='CANCEL':
                    
            CancelTemplateState(pk).handle_state()
                    
        elif request_name=='UPDATE':
            # TODO chain for update state of orders
        else:

            logging.error("A request does not have a valid state")
            raise Exception('NOT A VALID STATE')
        

class ConcreteChain(HandleRequestStateChain):
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

    def handle_request(self, class_name):
        """ 
        Create a class registered in Chain
        """ 
    
        return self.__state.handle()

