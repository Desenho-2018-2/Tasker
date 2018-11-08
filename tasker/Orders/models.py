from django.db import models

class Order(models.Model):
    """
    This model represent a order from the client.
    """

    # project id from extern service
    product_id = models.IntegerField()
    
    # source table
    table = models.IntegerField()

    # commentary about 
    comentary = models.TextField(max_length=500)
    
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()

    # TODO restrigir os valores do tipo
    order_type = models.IntegerField()

