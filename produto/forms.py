from django.forms.models import BaseInlineFormSet
from django import forms
from .models import Produto


class VariacaoObrigatoria(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(VariacaoObrigatoria, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('slug',)
