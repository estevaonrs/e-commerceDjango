from django.utils import timezone
import re
from django.utils.text import slugify

from django.contrib.auth.models import User
from django.utils.html import format_html

from django.db import models
from django.forms import ValidationError
from utils.validacpf import valida_cpf


class Cliente(models.Model):
    codigo = models.CharField(
        max_length=4, verbose_name='Código', blank=True, null=True)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário', blank=True, null=True)

    def __str__(self):
        return f'{self.usuario}'

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Fiado(models.Model):
    data = models.DateField(default=timezone.now,
                            verbose_name='Data da compra')
    data_p = models.DateField(default=timezone.now,
                              verbose_name='Data do pagamento')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,
                                default=None, blank=True, null=True, verbose_name="Cliente")
    valor = models.FloatField(verbose_name="Valor da dívida")
    pagamento = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('C', 'Cartão'),
            ('D', 'Dinheiro'),
        )
    )
    status = models.CharField(
        default="D",
        max_length=1,
        choices=(
            ('D', 'Devendo'),
            ('P', 'Pago'),
        )
    )


class ContasReceber(models.Model):
    data = models.DateField(verbose_name="Data do pagamento")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,
                                default=None, blank=True, null=True, verbose_name="Cliente")
    valor = models.FloatField(verbose_name="Valor da dívida")
    pagamento = models.CharField(
        max_length=100, verbose_name="Tipo de pagamento")
    status = models.CharField(
        default="D",
        max_length=1,
        choices=(
            ('D', 'Devendo'),
            ('P', 'Pago'),
        )
    )

    class Meta:
        verbose_name = 'Contas a receber'
        verbose_name_plural = 'Contas a receber'
