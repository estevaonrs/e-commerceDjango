from django.contrib import admin
from . import models


class CaixaAberto(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'status', 'data']


admin.site.register(models.CaixaAberto, CaixaAberto)
