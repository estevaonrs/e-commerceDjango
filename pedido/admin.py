from django.contrib import admin

from . import models


class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    ist_display = ['usuario', 'total',
                   'qtd_total', 'status']
    inlines = [
        ItemPedidoInline
    ]


admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.ItemPedido)
