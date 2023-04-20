from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Vendedor(models.Model):
    vendedor = models.CharField(max_length=100, verbose_name="Vendedor(a)")
    comissao = models.FloatField(verbose_name="Comissão")

    def __str__(self):
        return self.vendedor

    class Meta:
        verbose_name = 'Vendedor(a)'
        verbose_name_plural = 'Vendedores'
