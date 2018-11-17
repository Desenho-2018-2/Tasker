from os.path import join

from django.db import models
from Orders.models import Order

class Observer(models.Model):
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    link = models.CharField(max_length=100)

    def __str__(self):
        return join(self.ip, str(self.port), self.link)

class Target(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    observer = models.ForeignKey(Observer, on_delete=models.DO_NOTHING)
