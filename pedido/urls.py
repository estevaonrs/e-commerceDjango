from django.urls import path

from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
    path('lista_admin/', views.lista_admin.as_view(), name='lista_admin'),
    path('detalhe_admin/<int:pk>',
         views.detalhe_admin, name='detalhe_admin'),
    path('pedido/<int:pk>/excluir/', views.excluir_pedido, name='excluir_pedido'),


]
