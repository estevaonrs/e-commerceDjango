from django.contrib import admin
from . import models


class CaixaAberto(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'status', 'data']


class Reforço(admin.ModelAdmin):
    list_display = ['reforço']


class Retirada(admin.ModelAdmin):
    list_display = ['retirada']


admin.site.register(models.CaixaAberto, CaixaAberto)
admin.site.register(models.Reforço, Reforço)
admin.site.register(models.Retirada, Retirada)
