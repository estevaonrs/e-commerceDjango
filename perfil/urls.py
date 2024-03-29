from django.urls import path

from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('lista_perfis/', views.PerfilListView.as_view(),
         name='lista_perfis'),
    path('buscar_perfil/', views.buscar_perfil,
         name='buscar_perfil'),

]
