from django.urls import path

from . import views

app_name = 'gestao'

urlpatterns = [
    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),
    path('dashboard/', views.Dashboard.as_view(),
         name='dashboard'),
    path('produtos_mais_vendidos/', views.TopProdutosView,
         name='produtos_mais_vendidos'),
    path('clientes_mais_compram/', views.TopPerfisView,
         name='clientes_mais_compram'),
    path('caixa/', views.Caixa.as_view(),
         name='caixa'),
    path('lista_caixa/', views.CaixaAberto.as_view(),
         name='lista_caixa'),
    path('caixas/<int:pk>/', views.CaixaAbertoDetail.as_view(),
         name='caixa_aberto_detail'),
    path('caixa_aberto/<int:pk>/reforco/',
         views.reforco_caixa, name='reforco_caixa'),
    path('caixa_aberto/<int:pk>/retirada/',
         views.retirada_caixa, name='retirada_caixa'),




]
