from django.shortcuts import render
from django.urls import reverse_lazy

from vendas.forms import VendedorForm
from django.views.generic.edit import CreateView
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
