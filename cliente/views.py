from datetime import datetime
from .forms import FiadoForm
from django.shortcuts import render, redirect
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Cliente, Fiado
from .forms import ClienteForm, FiadoForm


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_create.html'
    success_url = reverse_lazy('produto:cadastros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Cliente'
        return context


class FiadoCreateView(CreateView):
    model = Fiado
    form_class = FiadoForm
    template_name = 'fiado_create.html'
    success_url = reverse_lazy('gestao:gestao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Fiado'
        return context

    def form_valid(self, form):
        fiado = form.save(commit=False)
        fiado.save()
        return super().form_valid(form)
