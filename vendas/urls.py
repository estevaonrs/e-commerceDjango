from django.conf import settings
from django.urls import path
from .views import VendedorCreateView, Vendas, VendedoresListView

app_name = 'vendas'

urlpatterns = [
    path('novo_vendedor/', VendedorCreateView.as_view(),
         name='vendedor_create'),
    path('lista_vendas/', Vendas.as_view(),
         name='vendas'),
    path('lista_vendedores/', VendedoresListView.as_view(),
         name='lista_vendedores'),
]
