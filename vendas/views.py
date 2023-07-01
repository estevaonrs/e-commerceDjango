from django.shortcuts import render
from django.urls import reverse_lazy
from vendas import models
from pedido.models import Pedido
from vendas.forms import VendedorForm
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from .models import Vendedor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class VendedorCreateView(LoginRequiredMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor_create.html'
    success_url = reverse_lazy('vendas:lista_vendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Vendedor(a)'
        return context


class Vendas(LoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidosadmin'
    template_name = 'vendas/lista_vendas.html'
    paginate_by = 10
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendedores'] = models.Vendedor.objects.all()
        return context


class VendedoresListView(LoginRequiredMixin, ListView):
    model = Vendedor
    context_object_name = 'vendedores'
    template_name = 'vendas/lista_vendedores.html'
    paginate_by = 10
    ordering = ['-id']


class VendedoresUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor_create.html'
    success_url = reverse_lazy('vendas:lista_vendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Vendedor'
        return context


class VendedoresDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendedor
    template_name = 'vendedor_delete.html'
    success_url = reverse_lazy('vendas:lista_vendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Vendedor?'
        return context


def buscar_venda(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Pedido.objects.filter(
            Q(vendedor__vendedor__icontains=query))

    return render(request, 'vendas/lista_vendas.html', {'pedidosadmin': resultados})
