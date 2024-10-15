from django.db import models
from users.users.models import *

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

