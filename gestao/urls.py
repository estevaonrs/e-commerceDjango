from django.urls import path

from . import views

app_name = 'gestao'

urlpatterns = [
    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),
    path('dashboard/', views.Dashboard.as_view(),
         name='dashboard'),
    path('produtos_mais_vendidos/', views.TopProdutosView,
         name='produtos_mais_vendidos'),
    path('venas_gerais/', views.VendasGeraisView,
         name='vendas_gerais'),
    path('relatorio_financeiro/', views.RelatorioFinanceiroView,
         name='relatorio_financeiro'),
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
    path('buscar_caixa_aberto', views.buscar_caixa_aberto,
         name='buscar_caixa_aberto'),
    path('perfil_detalhe/<int:perfil_id>/',
         views.PerfilDetalheView, name='perfil_detalhe'),
    path('perfil_detalhe/<int:perfil_id>/<str:tipo_venda>/',
         views.PerfilDetalheView, name='perfil_detalhe_tipo_venda'),
    path('relatorio_caixa_por_data/', views.RelatorioCaixaPorDataView.as_view(),
         name='relatorio_caixa_por_data'),





]
