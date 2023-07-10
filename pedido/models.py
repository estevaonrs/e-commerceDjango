from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from vendas.models import Vendedor


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('C', 'Criado'),
            ('A', 'Aprovado'),
        )
    )
    data = models.DateField(default=timezone.now,
                            verbose_name='Data do pedido')
    pagamento = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('C', 'Cartão'),
            ('D', 'Dinheiro'),
        )
    )
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, blank=True, null=True)

    @staticmethod
    def obter_quantidade_aprovados_por_dia(data):
        return Pedido.objects.filter(status='A', data=data).count()

    def __str__(self):
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_modalidade = models.CharField(
        max_length=255, blank=True, null=True)
    produto_cor = models.CharField(max_length=255, blank=True, null=True)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'


class Devolucao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    pagamento = models.CharField(
        max_length=255, verbose_name="Tipo de pagamento")
    observacoes = models.CharField(
        max_length=255, verbose_name="Observações")

    data = models.DateField(default=timezone.now,
                            verbose_name='Data da devolução')

    def __str__(self):
        return f'Devolução do pedido {self.pedido}'

    class Meta:
        verbose_name = 'Devolução do pedido'
        verbose_name_plural = 'Devoluções do pedido'


class Cupom(models.Model):
    codigo = models.CharField(max_length=50)
    valor = models.FloatField()

    def __str__(self):
        return self.codigo
