from datetime import datetime
from utils.utils import cart_totals

from .forms import FiadoForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cliente, Fiado, ContasReceber
from .forms import ClienteForm, FiadoForm, ContasReceberForm
from produto.models import Categoria, Produto, Tipo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import threading

from django.db.models import Q


@login_required
def codigo_acesso(request):
    perfil = Cliente.objects.filter(usuario=request.user).first()

    # Verificar se o cliente já digitou o código de acesso nesta sessão
    codigo_acesso_digitado = request.session.get(
        'codigo_acesso_digitado', False)

    if not codigo_acesso_digitado:
        if not perfil or not perfil.codigo:
            return render(request, 'codigo_acesso.html', {'erro': 'Você não tem acesso ao catálogo de atacado, fale com a loja!'})
        else:
            # Se o perfil do cliente possui o código, mas ainda não foi digitado nesta sessão, solicite o código.
            if request.method == 'POST':
                codigo_digitado = request.POST.get('codigo', '')

                if codigo_digitado == perfil.codigo:
                    # Se o código estiver correto, armazene o indicador na sessão
                    request.session['codigo_acesso_digitado'] = True

                    nomes_produtos = Produto.objects.values_list(
                        'nome', flat=True).distinct()
                    produtos = Produto.objects.filter(
                        nome__in=nomes_produtos, is_primary=True).order_by('-destaque', '-id')
                    categorias = Categoria.objects.all()
                    tipos = Tipo.objects.all()

                    context = {
                        'produtos': produtos,
                        'categorias': categorias,
                        'tipos': tipos
                    }

                    # Acessar o carrinho da sessão e adicionar ao contexto
                    carrinho = request.session.get('carrinho', {})
                    totals = cart_totals(carrinho)
                    context['carrinho'] = carrinho
                    context['cart_totals'] = totals

                    return render(request, 'produto/lista_atacado.html', context)
                else:
                    return render(request, 'codigo_acesso.html', {'erro': 'Código inválido.'})
            else:
                return render(request, 'codigo_acesso.html')

    # Se o código já foi digitado nesta sessão e é válido, redirecione para a lista_atacado
    nomes_produtos = Produto.objects.values_list(
        'nome', flat=True).distinct()
    produtos = Produto.objects.filter(
        nome__in=nomes_produtos, is_primary=True).order_by('-destaque', '-id')
    categorias = Categoria.objects.all()
    tipos = Tipo.objects.all()

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'tipos': tipos
    }

    # Acessar o carrinho da sessão e adicionar ao contexto
    carrinho = request.session.get('carrinho', {})
    totals = cart_totals(carrinho)
    context['carrinho'] = carrinho
    context['cart_totals'] = totals

    return render(request, 'produto/lista_atacado.html', context)


def reset_codigo_cliente():
    # Obtenha todos os clientes e redefine o campo 'codigo' para 0, exceto para os clientes com código permanente
    clientes = Cliente.objects.filter(codigo_permanente=False)
    for cliente in clientes:
        cliente.codigo = 0
        cliente.save()


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_create.html'
    success_url = reverse_lazy('cliente:lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Revendedor'
        return context

    def dispatch(self, request, *args, **kwargs):
        # Inicie uma nova thread para chamar a função reset_codigo_cliente após 1 minuto
        t = threading.Timer(172800, reset_codigo_cliente)
        t.start()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data['codigo_permanente']:
            self.object.tornar_codigo_permanente()
        return response


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    context_object_name = 'clientes'
    template_name = 'cliente/lista_clientes.html'
    paginate_by = 10
    ordering = ['-id']


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_create.html'
    success_url = reverse_lazy('cliente:lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Revendedor'
        return context


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cliente_delete.html'
    success_url = reverse_lazy('cliente:lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Revendedor'
        return context


class ContasReceberCreateView(LoginRequiredMixin, CreateView):
    model = ContasReceber
    form_class = ContasReceberForm
    template_name = 'contasreceber_create.html'
    success_url = reverse_lazy('cliente:lista_contasreceber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Conta a Receber'
        return context


class ContasReceberListView(LoginRequiredMixin, ListView):
    model = ContasReceber
    context_object_name = 'contasreceber'
    template_name = 'cliente/lista_contasreceber.html'
    paginate_by = 10
    ordering = ['-id']


class ContasReceberUpdateView(LoginRequiredMixin, UpdateView):
    model = ContasReceber
    form_class = ContasReceberForm
    template_name = 'contasreceber_create.html'
    success_url = reverse_lazy('cliente:lista_contasreceber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Conta a Receber'
        return context


class ContasReceberDeleteView(LoginRequiredMixin, DeleteView):
    model = ContasReceber
    template_name = 'contasreceber_delete.html'
    success_url = reverse_lazy('cliente:lista_contasreceber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Conta a Receber'
        return context


class FiadoCreateView(LoginRequiredMixin, CreateView):
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


class lista_fiado(LoginRequiredMixin, ListView):
    model = Fiado
    context_object_name = 'fiados'
    template_name = 'cliente/lista_fiado.html'
    paginate_by = 10
    ordering = ['-id']


class FiadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Fiado
    form_class = FiadoForm
    template_name = 'fiado_create.html'
    success_url = reverse_lazy('cliente:lista_fiado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Fiado'
        return context


class FiadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Fiado
    template_name = 'fiado_delete.html'
    success_url = reverse_lazy('cliente:lista_fiado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Fiado?'
        return context


def buscar_fiado(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Fiado.objects.filter(Q(cliente__nome__icontains=query))

    return render(request, 'cliente/lista_fiado.html', {'fiados': resultados})


def buscar_conta_receber(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = ContasReceber.objects.filter(
            Q(cliente__nome__icontains=query))

    return render(request, 'cliente/lista_contasreceber.html', {'contasreceber': resultados})


def buscar_revendedor(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Cliente.objects.filter(
            Q(usuario__username__icontains=query))

    return render(request, 'cliente/lista_clientes.html', {'clientes': resultados})
