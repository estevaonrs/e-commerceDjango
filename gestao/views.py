from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, CreateView
from . models import CaixaAberto
from . forms import CaixaAbertoForm
from pedido.models import Devolucao, Pedido
from cliente.models import ContasReceber
from produto.models import ContasPagar
from django.views.generic.detail import DetailView
from datetime import date
from django.db.models import Sum, Avg

from gestao import models


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
        total_pedidos = pedidos_aprovados.aggregate(Sum('total'))['total__sum']
        valor_medio_vendas = pedidos_aprovados.aggregate(Avg('total'))[
            'total__avg']
        soma_devolucoes = devolucoes.aggregate(Sum('pedido__total'))[
            'pedido__total__sum']
        context['data_caixa'] = data_caixa
        context['pedidos_aprovados'] = pedidos_aprovados
        context['quantidade_aprovados'] = quantidade_aprovados
        context['devolucoes'] = devolucoes
        context['total_pedidos'] = total_pedidos
        context['valor_medio_vendas'] = valor_medio_vendas
        context['soma_devolucoes'] = soma_devolucoes
        return context


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
