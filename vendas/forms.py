from django import forms
from .models import Vendedor


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = '__all__'
