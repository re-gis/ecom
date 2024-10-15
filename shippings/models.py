from django.db import models


# Create your models here.
class ShippingAddress(models.Model):
    customer = models.ForeignKey('users.Customer', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("orders.Order", models.SET_NULL, null=True)
    district = models.CharField(max_length=255, null=False)
    sector = models.CharField(max_length=255, null=False)
    zipcode = models.CharField(max_length=255, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
