from datetime import datetime

from .forms import FiadoForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cliente, Fiado, ContasReceber
from .forms import ClienteForm, FiadoForm, ContasReceberForm
from produto.models import Produto


from django.contrib.auth.decorators import login_required


@login_required
def codigo_acesso(request):
    perfil = Cliente.objects.filter(usuario=request.user).first()

    if not perfil or not perfil.codigo:
        return render(request, 'codigo_acesso.html', {'erro': 'Você não tem acesso ao catálogo de atacado, fale com a loja!.'})

    if request.method == 'POST':
        codigo_digitado = request.POST.get('codigo', '')

        if codigo_digitado == perfil.codigo:
            produtos = Produto.objects.all()
            context = {
                'produtos': produtos, }
            return render(request, 'produto/lista_atacado.html', context)

        else:
            return render(request, 'codigo_acesso.html', {'erro': 'Código inválido.'})

    return render(request, 'codigo_acesso.html')


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_create.html'
    success_url = reverse_lazy('cliente:lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Revendedor'
        return context


class ClienteListView(ListView):
    model = Cliente
    context_object_name = 'clientes'
    template_name = 'cliente/lista_clientes.html'
    paginate_by = 10
    ordering = ['-id']


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_create.html'
    success_url = reverse_lazy('cliente:lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Revendedor'
        return context


class ClienteDeleteView(DeleteView):
    model = ContasReceber
    template_name = 'cliente_delete.html'
    success_url = reverse_lazy('cliente:lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Revendedor'
        return context


class ContasReceberCreateView(CreateView):
    model = ContasReceber
    form_class = ContasReceberForm
    template_name = 'contasreceber_create.html'
    success_url = reverse_lazy('cliente:lista_contasreceber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Conta a Receber'
        return context


class ContasReceberListView(ListView):
    model = ContasReceber
    context_object_name = 'contasreceber'
    template_name = 'cliente/lista_contasreceber.html'
    paginate_by = 10
    ordering = ['-id']


class ContasReceberUpdateView(UpdateView):
    model = ContasReceber
    form_class = ContasReceberForm
    template_name = 'contasreceber_create.html'
    success_url = reverse_lazy('cliente:lista_contasreceber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Conta a Receber'
        return context


class ContasReceberDeleteView(DeleteView):
    model = ContasReceber
    template_name = 'contasreceber_delete.html'
    success_url = reverse_lazy('cliente:lista_contasreceber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Conta a Receber'
        return context


class FiadoCreateView(CreateView):
    model = Fiado
    form_class = FiadoForm
    template_name = 'fiado_create.html'
    success_url = reverse_lazy('cliente:lista_fiado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Fiado'
        return context

    def form_valid(self, form):
        fiado = form.save(commit=False)
        fiado.save()
        return super().form_valid(form)


class lista_fiado(ListView):
    model = Fiado
    context_object_name = 'fiados'
    template_name = 'cliente/lista_fiado.html'
    paginate_by = 10
    ordering = ['-id']


class FiadoUpdateView(UpdateView):
    model = Fiado
    form_class = FiadoForm
    template_name = 'fiado_create.html'
    success_url = reverse_lazy('cliente:lista_fiado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Fiado'
        return context


class FiadoDeleteView(DeleteView):
    model = Fiado
    template_name = 'fiado_delete.html'
    success_url = reverse_lazy('cliente:lista_fiado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Fiado?'
        return context
