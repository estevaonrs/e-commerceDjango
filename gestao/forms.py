from django import forms
from . import models


class CaixaForm(forms.ModelForm):
    class Meta:
        model = models.Caixa
        fields = '__all__'
