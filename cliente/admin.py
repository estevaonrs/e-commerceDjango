from django.contrib import admin

from . import models


class FiadoAdmin(admin.ModelAdmin):
    list_display = ['data', 'cliente',
                    'valor', 'pagamento']


class ContasReceberAdmin(admin.ModelAdmin):
    list_display = ['data', 'cliente',
                    'valor', 'pagamento']


admin.site.register(models.Cliente)
admin.site.register(models.Fiado, FiadoAdmin)
admin.site.register(models.ContasReceber, ContasReceberAdmin)
