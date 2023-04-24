from django.conf import settings
from django.urls import path
from .views import VendedorCreateView
from . import views

app_name = 'vendas'

urlpatterns = [
    path('novo_vendedor/', VendedorCreateView.as_view(),
         name='vendedor_create'),
]
