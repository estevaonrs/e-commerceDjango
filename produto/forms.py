from django.forms.models import BaseInlineFormSet
from django import forms
from .models import Influenciadores, Produto, Variacao, ImagemProduto, Categoria, Fornecedor, ContasPagar, Tipo


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'


class CategoriaForm(forms.ModelForm):
    MODALIDADE_CHOICES = (
        ('A', 'Atacado'),
        ('V', 'Varejo'),
    )
    modalidade = forms.ChoiceField(
        choices=MODALIDADE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Categoria
        fields = ('nome', 'modalidade', 'imagem')


class TipoForm(forms.ModelForm):
    MODALIDADE_CHOICES = (
        ('A', 'Atacado'),
        ('V', 'Varejo'),
    )
    modalidade = forms.ChoiceField(
        choices=MODALIDADE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Tipo
        fields = ('nome', 'modalidade')


class ContasPagarForm(forms.ModelForm):
    class Meta:
        model = ContasPagar
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


class VariacaoObrigatoria(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(VariacaoObrigatoria, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personaliza as opções de exibição para o campo categoria
        self.fields['categoria'].label_from_instance = self.label_from_instance_categoria

        # Personaliza as opções de exibição para o campo tipo
        self.fields['tipo'].label_from_instance = self.label_from_instance_tipo

    def label_from_instance_categoria(self, obj):
        return f'{obj.nome} ({obj.modalidade})'

    def label_from_instance_tipo(self, obj):
        return f'{obj.nome} ({obj.modalidade})'


class ImagemProdutoForm(forms.ModelForm):
    imagens = forms.FileField(widget=forms.FileInput, required=False)

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


class InfluenciadoresForm(forms.ModelForm):
    variacao = forms.ModelChoiceField(
        queryset=Variacao.objects.all(),
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        produtos = Produto.objects.all()
        self.fields['produto'].queryset = produtos
        self.fields['produto'].label_from_instance = self.label_from_instance_with_modalidade

    def label_from_instance_with_modalidade(self, obj):
        return f'{obj.nome} - {obj.modalidade}'

    class Meta:
        model = Influenciadores
        fields = ['produto', 'nome', 'data', 'quantidade']
