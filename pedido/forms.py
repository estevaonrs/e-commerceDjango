from .models import Devolucao
from django import forms


class DevolucaoForm(forms.ModelForm):
    class Meta:
        model = Devolucao
        fields = '__all__'
