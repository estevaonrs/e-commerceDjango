from django.contrib import admin
from . import models


class VendedorAdmin(admin.ModelAdmin):
    list_display = ['vendedor', 'comissao',]


admin.site.register(models.Vendedor, VendedorAdmin)
