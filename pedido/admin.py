from django.contrib import admin

from . import models


class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'total',
                    'qtd_total', 'status', 'data', 'pagamento', 'vendedor']
    inlines = [
        ItemPedidoInline
    ]


class DevolucaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pedido', 'itens',
                    'pagamento', 'observacoes']


class CupomAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor']


admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.ItemPedido)
admin.site.register(models.Cupom)

admin.site.register(models.Devolucao, DevolucaoAdmin)
