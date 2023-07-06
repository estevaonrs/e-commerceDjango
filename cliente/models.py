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
    codigo_permanente = models.BooleanField(
        default=False, verbose_name='Código permanente')
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def tornar_codigo_permanente(self):
        self.codigo_permanente = True
        self.save()

    def __str__(self):
        return f'{self.nome}'

    def clean(self):
        error_messages = {}

        # Remover espaços em branco
        self.bairro = self.bairro.strip()
        self.cidade = self.cidade.strip()

        # Converter para maiúsculas
        self.bairro = self.bairro.upper()
        self.cidade = self.cidade.upper()

        # Remover acentuação
        self.bairro = slugify(self.bairro, allow_unicode=True)
        self.cidade = slugify(self.cidade, allow_unicode=True)

        # Verificar se o campo está vazio após as transformações
        if not self.bairro:
            error_messages['bairro'] = 'O campo Bairro é obrigatório.'

        if not self.cidade:
            error_messages['cidade'] = 'O campo Cidade é obrigatório.'

        # Verificar se já existem 2 clientes com mesma cidade e bairro
        clientes_mesma_cidade_bairro = Cliente.objects.filter(
            cidade=self.cidade, bairro=self.bairro)
        if self.pk:
            # Excluir o cliente atual da contagem
            clientes_mesma_cidade_bairro = clientes_mesma_cidade_bairro.exclude(
                pk=self.pk)
        if clientes_mesma_cidade_bairro.count() >= 2:
            error_messages['bairro'] = format_html('Já existem 2 clientes para esse mesmo Bairro: {}',
                                                   self.bairro)

        if error_messages:
            raise ValidationError(error_messages)

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 dígitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)

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
