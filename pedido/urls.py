from django.urls import path

from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:id>', views.pagar, name='pagar'),
    path('pedido_sucesso/', views.SucessoView.as_view(), name='pedido_sucesso'),

    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('salvarpedido_admin/', views.SalvarPedidoAdmin.as_view(),
         name='salvarpedido_admin'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
    path('lista_admin/', views.lista_admin.as_view(), name='lista_admin'),
    path('detalhe_admin/<int:pk>',
         views.detalhe_admin, name='detalhe_admin'),
    path('pedido/<int:pk>/excluir/', views.excluir_pedido, name='excluir_pedido'),
    path('nova_devolucao/', views.DevolucaoCreateView.as_view(),
         name='devolucao_create'),
    path('criar_novo_pedido/', views.criar_novo_pedido.as_view(),
         name='criar_novo_pedido'),
    path('lista_devolucao/', views.DevolucaoListView.as_view(),
         name='lista_devolucao'),
    path('devolucao_edit/<int:pk>/',
         views.DevolucaoUpdateView.as_view(), name='devolucao_edit'),
    path('devolucao_delete/<int:pk>/',
         views.DevolucaoDeleteView.as_view(), name='devolucao_delete'),
    path('pedido_edit/<int:pk>/',
         views.PedidoUpdateView.as_view(), name='pedido_edit'),





]
