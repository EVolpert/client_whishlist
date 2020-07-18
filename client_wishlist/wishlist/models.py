from django.contrib.postgres.fields import JSONField
from django.db import models

from customers.models import Customer


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, unique=True)
    wishlist = JSONField()

    def __str__(self):
        return f'Lista de desejos de {self.customer.name}'
