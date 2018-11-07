from django.db import models

class Orders(models.Model):
    id = models.IntegerField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)


