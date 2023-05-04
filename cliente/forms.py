from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from . import models


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = '__all__'


class FiadoForm(forms.ModelForm):
    class Meta:
        model = models.Fiado
        fields = ['data', 'cliente', 'valor', 'pagamento']
        widgets = {
            'data': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }


class ContasReceberForm(forms.ModelForm):
    class Meta:
        model = models.ContasReceber
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }
