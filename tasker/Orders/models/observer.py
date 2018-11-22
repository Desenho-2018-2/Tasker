import logging 

from os.path import join
from django.db import models
from Orders.models import Order

class Observer(models.Model):
    """
    Save in database the observer pattern
    """

    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    link = models.CharField(max_length=100)

    orders = models.ManyToManyField(Order,
                                    blank=True)

    def __str__(self):

        string_response = join(self.ip + ':'  + str(self.port), self.link)

        logging.warn(string_response)
        
        return string_response

    class Meta:
        unique_together = (('ip', 'port', 'link'))
