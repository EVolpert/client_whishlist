from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200, help_text="Nome do cliente", verbose_name="Nome")
    email = models.EmailField(unique=True, help_text="Endereço de Email", verbose_name="Email")

    def __str__(self):
        return self.name
