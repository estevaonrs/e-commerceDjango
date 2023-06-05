from .models import Devolucao, Pedido
from django import forms


class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = Devolucao
        fields = '__all__'


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status', 'data', 'pagamento', 'vendedor']
