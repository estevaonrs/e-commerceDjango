from django.db import models


class Caixa(models.Model):
    nome = models.CharField(max_length=65, verbose_name='Apelido do Caixa')
    valor = models.FloatField(verbose_name='Valor de Abertura')

    def __str__(self):
        return self.nome
