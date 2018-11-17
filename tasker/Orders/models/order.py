from django.db import models

WAITING_CONST = 'WAIT'
COOKING_CONST = 'COOK'
DONE_CONST = 'DONE'
PICKIT_CONST = 'PICKIT'
CLOSE_CONST = 'CLOSE'
CANCEL_CONST = 'CANCEL'

DRINK_TYPE = 'DRINK'
FOOD_TYPE = 'FOOD'

class Order(models.Model):
    """
    This model represent a order from the client.
    """

    ORDER_STATUS = ((WAITING_CONST, 'WAITING'),
                    (COOKING_CONST, 'COOKING'),
                    (DONE_CONST, 'DONE'),
                    (PICKIT_CONST, 'PICKIT'),
                    (CLOSE_CONST, 'CLOSE'),
                    (CANCEL_CONST, 'CANCEL'))

    ORDER_TYPE = ((DRINK_TYPE, 'DRINK'),
                  (FOOD_TYPE, 'FOOD'))

    # project id from extern service
    product_id = models.IntegerField()

    # source table
    table = models.IntegerField()

    # commentary about
    comentary = models.TextField(max_length=500)

    date = models.DateField(auto_now_add=True)
    time = models.TimeField()

    # TODO restrigir os valores do tipo
    order_type = models.CharField(choices=ORDER_TYPE,
                                  max_length=12,
                                  default=FOOD_TYPE)

    # state of a order in queue
    state = models.CharField(choices=ORDER_STATUS,
                             max_length=12,
                             default=WAITING_CONST)

