from django.conf import settings
from django.urls import path
from .views import VendedorCreateView, Vendas, VendedoresListView, VendedoresUpdateView, VendedoresDeleteView
app_name = 'vendas'

urlpatterns = [
    path('novo_vendedor/', VendedorCreateView.as_view(),
         name='vendedor_create'),
    path('lista_vendas/', Vendas.as_view(),
         name='vendas'),
    path('lista_vendedores/', VendedoresListView.as_view(),
         name='lista_vendedores'),
    path('vendedor_edit/<int:pk>/',
         VendedoresUpdateView.as_view(), name='vendedor_edit'),
    path('vendedor_delete/<int:pk>/',
         VendedoresDeleteView.as_view(), name='vendedor_delete'),


]
