from django.shortcuts import render
from django.urls import reverse_lazy
from pedido.models import Pedido
from vendas.forms import VendedorForm
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from .models import Vendedor


class VendedorCreateView(CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor_create.html'
    success_url = reverse_lazy('produto:cadastros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Vendedor(a)'
        return context


class Vendas(ListView):
    model = Pedido
    context_object_name = 'pedidosadmin'
    template_name = 'vendas/lista_vendas.html'
    paginate_by = 10
    ordering = ['-id']


class VendedoresListView(ListView):
    model = Vendedor
    context_object_name = 'vendedores'
    template_name = 'vendas/lista_vendedores.html'
    paginate_by = 10
    ordering = ['-id']
