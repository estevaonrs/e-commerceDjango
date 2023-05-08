from django.views.generic import ListView
from django.shortcuts import render
from django.views.generic import TemplateView


from pedido.models import Devolucao
from cliente.models import ContasReceber
from produto.models import ContasPagar


class GestaoView(TemplateView):
    template_name = 'gestao.html'


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
