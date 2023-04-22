from django.urls import path
from .views import ClienteCreateView


app_name = 'cliente'


urlpatterns = [
    path('novo/', ClienteCreateView.as_view(), name='cliente_create'),

]
