from django import forms
from . import models


class CaixaAbertoForm(forms.ModelForm):
    class Meta:
        model = models.CaixaAberto
        fields = ['nome', 'valor']


class ReforçoForm(forms.ModelForm):
    class Meta:
        model = models.Reforço
        fields = ['reforço']


class RetiradaForm(forms.ModelForm):
    class Meta:
        model = models.Retirada
        fields = ['retirada', 'observacao']
