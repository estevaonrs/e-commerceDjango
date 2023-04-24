from django.contrib import admin

from . import models


class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'total',
                    'qtd_total', 'status']
    inlines = [
        ItemPedidoInline
    ]


class DevolucaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pedido', 'itens',
                    'pagamento', 'observacoes']


admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.ItemPedido)
admin.site.register(models.Devolucao, DevolucaoAdmin)
