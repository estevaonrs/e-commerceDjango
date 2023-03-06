from django.forms.models import BaseInlineFormSet
from django import forms
from .models import Produto, Variacao, ImagemProduto, Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nome',)


class VariacaoObrigatoria(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(VariacaoObrigatoria, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('slug',)


class ImagemProdutoForm(forms.ModelForm):
    imagem = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ImagemProduto
        fields = ['imagem']


class VariacaoForm(forms.ModelForm):
    class Meta:
        model = Variacao
        fields = ['nome', 'preco', 'preco_promocional', 'estoque']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da variação'}),
            'preco': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'preco_promocional': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'estoque': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }
