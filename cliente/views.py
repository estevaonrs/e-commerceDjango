from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Cliente
from .forms import ClienteForm


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_create.html'
    success_url = reverse_lazy('produto:cadastros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Cliente'
        return context
