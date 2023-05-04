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


]
