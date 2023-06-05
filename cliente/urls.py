from django.urls import path

from cliente.models import ContasReceber
from .views import ClienteCreateView, ClienteDeleteView, ClienteListView, ClienteUpdateView, ContasReceberDeleteView,\
    ContasReceberListView, ContasReceberUpdateView, FiadoCreateView, \
    lista_fiado, ContasReceberCreateView, codigo_acesso, FiadoUpdateView, \
    FiadoDeleteView


app_name = 'cliente'


urlpatterns = [
    path('novo_cliente/', ClienteCreateView.as_view(), name='cliente_create'),
    path('novo_fiado/', FiadoCreateView.as_view(), name='fiado_create'),
    path('lista_fiado/', lista_fiado.as_view(), name='lista_fiado'),
    path('conta_receber/', ContasReceberCreateView.as_view(), name='conta_receber'),
    path('codigo-acesso/', codigo_acesso, name='codigo_acesso'),
    path('lista_contasreceber/', ContasReceberListView.as_view(),
         name='lista_contasreceber'),
    path('conta_receber_edit/<int:pk>/',
         ContasReceberUpdateView.as_view(), name='conta_receber_edit'),
    path('conta_receber_delete/<int:pk>/',
         ContasReceberDeleteView.as_view(), name='conta_receber_delete'),
    path('fiado_edit/<int:pk>/',
         FiadoUpdateView.as_view(), name='fiado_edit'),
    path('fiado_delete/<int:pk>/',
         FiadoDeleteView.as_view(), name='fiado_delete'),
    path('lista_clientes/', ClienteListView.as_view(),
         name='lista_clientes'),
    path('cliente_edit/<int:pk>/',
         ClienteUpdateView.as_view(), name='cliente_edit'),
    path('cliente_delete/<int:pk>/',
         ClienteDeleteView.as_view(), name='cliente_delete'),
]
