from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView
from . models import CaixaAberto, Retirada, Reforço
from . forms import CaixaAbertoForm, ReforçoForm, RetiradaForm
from pedido.models import Devolucao, Pedido
from cliente.models import ContasReceber, Fiado
from produto.models import ContasPagar
from django.views.generic.detail import DetailView
from datetime import date
from django.db.models import Sum, Avg


class GestaoView(TemplateView):
    template_name = 'gestao.html'


class DetalheCaixa(TemplateView):
    template_name = 'gestao/detalhe_caixa.html'


class CaixaAbertoDetail(DetailView):
    model = CaixaAberto
    context_object_name = 'caixa'
    template_name = 'gestao/caixa_aberto_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caixa = self.get_object()
        data_caixa = caixa.data

        devolucoes = Devolucao.objects.filter(data=data_caixa)
        pedidos_aprovados = Pedido.objects.filter(status='A', data=data_caixa)
        quantidade_aprovados = pedidos_aprovados.count()

        soma_fiados = Fiado.objects.filter(
            data=data_caixa).aggregate(soma=Sum('valor'))['soma']
        total_pedidos = pedidos_aprovados.aggregate(
            total=Sum('total'))['total']
        valor_medio_vendas = pedidos_aprovados.aggregate(media=Avg('total'))[
            'media']
        soma_devolucoes = devolucoes.aggregate(
            soma=Sum('pedido__total'))['soma']
        soma_retiradas = Retirada.objects.filter(
            data=data_caixa).aggregate(soma=Sum('retirada'))['soma']
        soma_reforcos = Reforço.objects.filter(data=data_caixa).aggregate(soma=Sum('reforço'))['soma']

        context['soma_fiados'] = soma_fiados
        context['data_caixa'] = data_caixa
        context['pedidos_aprovados'] = pedidos_aprovados
        context['quantidade_aprovados'] = quantidade_aprovados
        context['devolucoes'] = devolucoes
        context['total_pedidos'] = total_pedidos
        context['valor_medio_vendas'] = valor_medio_vendas
        context['soma_devolucoes'] = soma_devolucoes
        context['reforco_form'] = ReforçoForm()
        context['retirada_form'] = RetiradaForm()
        context['soma_retiradas'] = soma_retiradas
        context['soma_reforcos'] = soma_reforcos

        return context


def reforco_caixa(request, pk):
    caixa = get_object_or_404(CaixaAbertoDetail.model, pk=pk)

    if request.method == 'POST':
        form = ReforçoForm(request.POST)
        if form.is_valid():
            reforco = form.save(commit=False)
            reforco.caixa_aberto = caixa
            reforco.save()
            return redirect('gestao:caixa_aberto_detail', pk=caixa.pk)

    return redirect('gestao:caixa_aberto_detail', pk=caixa.pk)


def retirada_caixa(request, pk):
    caixa = get_object_or_404(CaixaAbertoDetail.model, pk=pk)

    if request.method == 'POST':
        form = RetiradaForm(request.POST)
        if form.is_valid():
            retirada = form.save(commit=False)
            retirada.caixa_aberto = caixa
            retirada.save()
            return redirect('gestao:caixa_aberto_detail', pk=caixa.pk)

    return redirect('gestao:caixa_aberto_detail', pk=caixa.pk)


class Dashboard(TemplateView):
    template_name = 'dashboard.html'


class ListaDevolucao(ListView):
    model = Devolucao
    context_object_name = 'devolucoes'
    template_name = 'gestao/lista_devolucao.html'
    paginate_by = 10
    ordering = ['-id']


class ContasReceber(ListView):
    model = ContasReceber
    context_object_name = 'contasreceber'
    template_name = 'gestao/lista_contasreceber.html'
    paginate_by = 10
    ordering = ['-id']


class ContasPagar(ListView):
    model = ContasPagar
    context_object_name = 'contaspagar'
    template_name = 'gestao/lista_contaspagar.html'
    paginate_by = 10
    ordering = ['-id']


class Caixa(CreateView):
    model = CaixaAberto
    form_class = CaixaAbertoForm
    template_name = 'gestao/caixa_create.html'
    success_url = reverse_lazy('gestao:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Controle de Caixa'
        return context


class CaixaAberto(ListView):
    model = CaixaAberto
    context_object_name = 'caixas'
    template_name = 'gestao/lista_caixa.html'
    paginate_by = 10
    ordering = ['-id']
