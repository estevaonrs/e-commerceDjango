from django.db import models
from django.utils import timezone
from pedido.models import Devolucao


class CaixaAberto(models.Model):
    nome = models.CharField(max_length=65, verbose_name='Apelido do Caixa')
    valor = models.FloatField(verbose_name='Valor de Abertura')
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Aberto'),
            ('F', 'Fechado'),
        )
    )
    data = models.DateField(default=timezone.now,
                            verbose_name='Data de Abertura')
    devolucao = models.ForeignKey(
        Devolucao, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome
