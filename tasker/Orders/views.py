from rest_framework.decorators import api_view
from Orders.serializers import OrdersSerializer
from rest_framework.response import Response
from rest_framework import status
import logging 

@api_view(['POST', 'GET'])
def insert_order(request):
    """
    Insert a order in database
    """

    logging.debug("The function insert_orders has this data \
                    {}".format(request.data))

    if request.method == 'GET':
        return Response('consegui')

    elif request.method == 'POST':

        serializer = OrdersSerializer(data=request.data)

        if serializer.is_valid():
            logging.debug("The data is valid")
            serializer.save()
            return Response(serializer.data)
        else:
            logging.warn("The post method don't work: {}".format(request.data))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
