from django.urls import path
from .views import ClienteCreateView, FiadoCreateView, lista_fiado, ContasReceberCreateView, codigo_acesso


app_name = 'cliente'


urlpatterns = [
    path('novo_cliente/', ClienteCreateView.as_view(), name='cliente_create'),
    path('novo_fiado/', FiadoCreateView.as_view(), name='fiado_create'),
    path('lista_fiado/', lista_fiado.as_view(), name='lista_fiado'),
    path('conta_receber/', ContasReceberCreateView.as_view(), name='conta_receber'),
    path('codigo-acesso/', codigo_acesso, name='codigo_acesso'),

]