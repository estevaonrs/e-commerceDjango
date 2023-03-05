from django.contrib import admin
from django.forms import ClearableFileInput
from django.utils.html import format_html
from . import models
from .forms import VariacaoObrigatoria


class ImagemInline(admin.TabularInline):
    model = models.ImagemProduto
    extra = 3
    max_num = 10
    formfield_overrides = {
        models.ImagemProduto.imagem: {'widget': ClearableFileInput(attrs={'multiple': True})},
    }
    verbose_name_plural = ('Imagens')


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    formset = VariacaoObrigatoria
    min_num = 1
    extra = 0
    can_delete = True


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'categoria',
                    'get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [
        VariacaoInline,
        ImagemInline
    ]


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
admin.site.register(models.ImagemProduto)
admin.site.register(models.Categoria)
