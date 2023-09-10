from .models import Cupom, Devolucao, Pedido
from django import forms


class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = Devolucao
        fields = '__all__'


class CupomForm(forms.ModelForm):
    class Meta:
        model = Cupom
        fields = ['codigo', 'valor']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status', 'data', 'pagamento', 'vendedor', 'usuario']


class PagamentoForm(forms.Form):
    nome_cliente = forms.CharField(label='Nome do Cliente')
    cpf_cnpj = forms.CharField(label='CPF/CNPJ')
    numero_cartao = forms.CharField(
        label='Número do Cartão de Crédito')
    mes_validade = forms.CharField(label='Mês de Validade')
    ano_validade = forms.CharField(label='Ano de Validade')
    ccv = forms.CharField(label='CCV')
    email = forms.EmailField(
        label='Email')
    endereco = forms.CharField(label='Endereço')
    cep = forms.CharField(label='CEP')
    telefone = forms.CharField(label='Telefone')
