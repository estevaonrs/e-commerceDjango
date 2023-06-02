from django.utils import timezone
import re

from django.contrib.auth.models import User

from django.db import models
from django.forms import ValidationError
from utils.validacpf import valida_cpf


class Cliente(models.Model):
    codigo = models.CharField(max_length=4,
                              verbose_name='Código', blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,
                                   verbose_name='Usuário')
    nome = models.CharField(max_length=100,
                            verbose_name='Nome completo', blank=True, null=True)
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    cnpj = models.CharField(max_length=14, blank=True, null=True)
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

    def __str__(self):
        return f'{self.nome}'

    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Cliente.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já existe.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 digitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Fiado(models.Model):
    data = models.DateField(default=timezone.now,
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
