from django.urls import path

from . import views

app_name = 'gestao'

urlpatterns = [
    path('gestao/', views.GestaoView.as_view(), name='gestao'),
    path('lista_devolucao/', views.ListaDevolucao.as_view(), name='lista_devolucao'),
    path('lista_contasreceber/', views.ContasReceber.as_view(),
         name='lista_contasreceber'),
    path('lista_contaspagar/', views.ContasPagar.as_view(),
         name='lista_contaspagar'),
    path('dashboard/', views.Dashboard.as_view(),
         name='dashboard'),
    path('caixa/', views.Caixa.as_view(),
         name='caixa'),
    path('lista_caixa/', views.CaixaAberto.as_view(),
         name='lista_caixa'),
    path('caixas/<int:pk>/', views.CaixaAbertoDetail.as_view(),
         name='caixa_aberto_detail'),




]
