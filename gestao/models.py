from django.db import models
from django.utils import timezone
from pedido.models import Devolucao


class CaixaAberto(models.Model):
    nome = models.CharField(max_length=65, verbose_name='Apelido do Caixa')
    valor = models.FloatField(verbose_name='Valor de Abertura')
    status = models.CharField(
        default="A",
        max_length=1,
        choices=(
            ('A', 'Aberto'),
            ('F', 'Fechado'),
        )
    )
    data = models.DateField(default=timezone.now,
                            verbose_name='Data de Abertura')

    def __str__(self):
        return self.nome


class Reforço(models.Model):
    reforço = models.FloatField(verbose_name='Valor do Reforço')
    data = models.DateField(default=timezone.now,
                            verbose_name='Data do reforço')


class Retirada(models.Model):
    retirada = models.FloatField(verbose_name='Valor da Retirada')
    data = models.DateField(default=timezone.now,
                            verbose_name='Data da retirada')
