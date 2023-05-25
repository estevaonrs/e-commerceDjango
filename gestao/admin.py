from django.contrib import admin
from . import models


class Caixa(admin.ModelAdmin):
    list_display = ['nome', 'valor']


admin.site.register(models.Caixa, Caixa)
