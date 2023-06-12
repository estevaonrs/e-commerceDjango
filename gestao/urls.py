from django.urls import path

from . import views

app_name = 'gestao'

urlpatterns = [
    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),
    path('dashboard/', views.Dashboard.as_view(),
         name='dashboard'),
    path('produtos_mais_vendidos/', views.TopProdutosView,
         name='produtos_mais_vendidos'),
    path('todos_produtos_mais_vendidos/', views.TopTodosProdutosView,
         name='todos_produtos_mais_vendidos'),
    path('venas_gerais/', views.VendasGeraisView,
         name='vendas_gerais'),

    path('vendedores_que_mais_vendem/', views.TopVendedorView,
         name='vendedores_mais_vendem'),
    path('clientes_mais_compram/', views.TopPerfisView,
         name='clientes_mais_compram'),
    path('caixa/', views.Caixa.as_view(),
         name='caixa'),
    path('lista_caixa/', views.CaixaAbertoListView.as_view(),
         name='lista_caixa'),
    path('caixas/<int:pk>/', views.CaixaAbertoDetail.as_view(),
         name='caixa_aberto_detail'),
    path('caixa_aberto/<int:pk>/reforco/',
         views.reforco_caixa, name='reforco_caixa'),
    path('caixa_aberto/<int:pk>/retirada/',
         views.retirada_caixa, name='retirada_caixa'),
    path('caixa_edit/<int:pk>/',
         views.CaixaUpdateView.as_view(), name='caixa_edit'),
    path('caixa_delete/<int:pk>/',
         views.CaixaDeleteView.as_view(), name='caixa_delete'),




]
