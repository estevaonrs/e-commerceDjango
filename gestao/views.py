from .models import CaixaAberto
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView
from . models import CaixaAberto, Retirada, Reforço
from . forms import CaixaAbertoForm, ReforçoForm, RetiradaForm
from pedido.models import Devolucao, Pedido
from cliente.models import Fiado

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

        pedidos_c = Pedido.objects.filter(
            data=data_caixa, pagamento='C', status='A')
        quantidade_pedidos_c = pedidos_c.count()
        soma_quantidade_pedidos_c = pedidos_c.aggregate(soma=Sum('total'))[
            'soma'] or 0

        pedidos_d = Pedido.objects.filter(
            data=data_caixa, pagamento='D', status='A')
        quantidade_pedidos_d = pedidos_d.count()
        soma_quantidade_pedidos_d = pedidos_d.aggregate(soma=Sum('total'))[
            'soma'] or 0

        fiados = Fiado.objects.filter(data=data_caixa, status='P')
        soma_fiados = fiados.aggregate(soma=Sum('valor'))['soma'] or 0

        fiados_d = Fiado.objects.filter(data=data_caixa, status='D')
        diminuicao_fiados = - \
            (fiados_d.aggregate(soma=Sum('valor'))['soma'] or 0)

        total_pedidos = pedidos_aprovados.aggregate(
            total=Sum('total'))['total'] or 0
        valor_medio_vendas = pedidos_aprovados.aggregate(media=Avg('total'))[
            'media']
        soma_devolucoes = devolucoes.aggregate(
            soma=Sum('pedido__total'))['soma'] or 0
        soma_retiradas = Retirada.objects.filter(
            data=data_caixa).aggregate(soma=Sum('retirada'))['soma'] or 0
        soma_reforcos = Reforço.objects.filter(data=data_caixa).aggregate(soma=Sum('reforço'))['soma'] or 0

        saldo = caixa.valor + total_pedidos - soma_devolucoes + \
            soma_reforcos + soma_fiados - soma_retiradas + diminuicao_fiados

        context['quantidade_pedidos_c'] = quantidade_pedidos_c
        context['soma_quantidade_pedidos_c'] = soma_quantidade_pedidos_c
        context['quantidade_pedidos_d'] = quantidade_pedidos_d
        context['soma_quantidade_pedidos_d'] = soma_quantidade_pedidos_d
        context['soma_fiados'] = soma_fiados
        context['diminuicao_fiados'] = diminuicao_fiados
        context['saldo'] = saldo
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

    def post(self, request, *args, **kwargs):
        caixa = self.get_object()

        if 'reopen' in request.POST:
            # Verifica se o caixa está fechado antes de reabri-lo
            if caixa.status == 'F':
                caixa.status = 'A'
                caixa.save()
        else:
            # Verifica se o caixa está aberto antes de fechá-lo
            if caixa.status == 'A':
                caixa.status = 'F'
                caixa.save()

        return redirect('gestao:lista_caixa')


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
