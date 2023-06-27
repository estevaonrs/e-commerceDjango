from .models import Cupom, Devolucao, Pedido
from django import forms


class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = Devolucao
        fields = '__all__'


class CupomForm(forms.ModelForm):
    class Meta:
        model = Cupom
        fields = ['codigo']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status', 'data', 'pagamento', 'vendedor']


class PagamentoForm(forms.Form):
    nome_cliente = forms.CharField(label='Nome do Cliente', initial='Roberto')
    cpf_cnpj = forms.CharField(label='CPF/CNPJ', initial='24971563792')
    numero_cartao = forms.CharField(
        label='Número do Cartão de Crédito', initial='5162306219378829')
    mes_validade = forms.CharField(label='Mês de Validade', initial='05')
    ano_validade = forms.CharField(label='Ano de Validade', initial='2024')
    ccv = forms.CharField(label='CCV', initial='318')
    email = forms.EmailField(
        label='Email', initial='marcelo.almeida@gmail.com')
    endereco = forms.CharField(label='Endereço', initial='Rua XYZ, 123')
    cep = forms.CharField(label='CEP', initial='89223-005')
    telefone = forms.CharField(label='Telefone', initial='4738010919')
