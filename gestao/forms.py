from django import forms
from . import models


class CaixaAbertoForm(forms.ModelForm):
    class Meta:
        model = models.CaixaAberto
        fields = ['nome', 'valor']
