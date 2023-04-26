from django.urls import path
from .views import ClienteCreateView, FiadoCreateView


app_name = 'cliente'


urlpatterns = [
    path('novo_cliente/', ClienteCreateView.as_view(), name='cliente_create'),
    path('novo_fiado/', FiadoCreateView.as_view(), name='fiado_create'),

]
