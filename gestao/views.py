from django.views import View
from perfil.models import Perfil
from perfil.models import Perfil
from .models import CaixaAberto
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView
from . models import CaixaAberto, Retirada, Reforço
from . forms import CaixaAbertoForm, ReforçoForm, RetiradaForm
from pedido.models import Devolucao, Pedido, ItemPedido
from cliente.models import Fiado
from produto.models import Produto
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from produto.models import Produto
from datetime import date, datetime
from django.db.models import Sum, Avg, Count, F, Sum, Case, When, IntegerField, Subquery, OuterRef, Value, DecimalField
from django.db.models import Q
from django.db.models.functions import Coalesce
from collections import Counter

from vendas.models import Vendedor


class RelatorioView(LoginRequiredMixin, TemplateView):
    template_name = 'relatorio.html'


@login_required
def RelatorioFinanceiroView(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    itens_aprovados = ItemPedido.objects.filter(pedido__status='A')
    pedidos_aprovados = Pedido.objects.filter(status='A')
    devolucoes = Devolucao.objects.all()

    # Aplicar filtro de datas, se fornecidas
    if data_inicio and data_fim:
        itens_aprovados = itens_aprovados.filter(
            pedido__data__range=(data_inicio, data_fim))
        pedidos_aprovados = pedidos_aprovados.filter(
            data__range=(data_inicio, data_fim))

    produtos_quantidades = (
        itens_aprovados
        .values('produto', 'produto_id', 'produto_modalidade', 'produto_cor')
        .annotate(quantidade=Sum('quantidade'))
        .order_by('-quantidade')
    )

    perfis_pedidos_aprovados = Perfil.objects.annotate(
        num_pedidos_aprovados=Count('usuario__pedido', filter=Q(
            usuario__pedido__status='A', usuario__pedido__data__range=(data_inicio, data_fim))),
        total_pedidos_aprovados=Sum(
            Case(
                When(usuario__pedido__status='A', usuario__pedido__data__range=(
                    data_inicio, data_fim), then='usuario__pedido__total'),
                default=0,
                output_field=IntegerField()
            )
        ),
        modalidade_pedido=F('usuario__pedido__itempedido__produto_modalidade')
    ).order_by('-num_pedidos_aprovados')

    vendedores_pedidos_aprovados = Vendedor.objects.annotate(num_pedidos_aprovados=Count('pedido', filter=Q(
        pedido__status='A', pedido__data__range=(data_inicio, data_fim)))).order_by('-num_pedidos_aprovados')[:10]

    quantidade_aprovados = pedidos_aprovados.count()
    quantidade_itens_aprovados = pedidos_aprovados.aggregate(
        total_itens=Sum('qtd_total'))['total_itens'] or 0
    total_pedidos = pedidos_aprovados.aggregate(total_pedidos=Sum('total'))[
        'total_pedidos'] or 0
    quantidade_devolucoes = devolucoes.count()
    soma_devolucoes = devolucoes.aggregate(total_devolucoes=Sum('pedido__total'))[
        'total_devolucoes'] or 0

    context = {
        'produtos_quantidades': produtos_quantidades,
        'perfis_pedidos_aprovados': perfis_pedidos_aprovados,
        'vendedores_pedidos_aprovados': vendedores_pedidos_aprovados,
        'quantidade_aprovados': quantidade_aprovados,
        'quantidade_itens_aprovados': quantidade_itens_aprovados,
        'total_pedidos': total_pedidos,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'quantidade_devolucoes': quantidade_devolucoes,
        'soma_devolucoes': soma_devolucoes,
    }

    return render(request, 'gestao/relatorio_financeiro.html', context)


@login_required
def TopProdutosView(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    subquery = ItemPedido.objects.filter(
        produto=OuterRef('produto'),
        produto_cor=OuterRef('produto_cor'),
        pedido__status='A'
    ).annotate(
        preco_item=Case(
            When(preco_promocional__gt=0, then=F('preco_promocional')),
            default=F('preco'),
            output_field=DecimalField()
        )
    ).values('produto', 'produto_cor').annotate(
        total=Sum('preco_item')
    ).values('total')

    itens_aprovados = ItemPedido.objects.filter(pedido__status='A')

    # Aplicar filtro de datas, se fornecidas
    if data_inicio and data_fim:
        itens_aprovados = itens_aprovados.filter(
            pedido__data__range=(data_inicio, data_fim))

    produtos_quantidades = (
        itens_aprovados
        .values('produto', 'produto_cor', 'produto_modalidade')
        .annotate(quantidade=Sum('quantidade'))
        .annotate(pedido_total=Subquery(subquery))
        .order_by('-quantidade')[:10]
    )

    context = {
        'produtos_quantidades': produtos_quantidades,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(request, 'gestao/produtos_mais_vendidos.html', context)


@login_required
def TopPerfisView(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    pedidos_aprovados = Pedido.objects.filter(status='A')
    # Aplicar filtro de datas, se fornecidas
    if data_inicio and data_fim:
        pedidos_aprovados = pedidos_aprovados.filter(
            data__range=(data_inicio, data_fim))

    perfis_pedidos_aprovados = Perfil.objects.annotate(
        num_pedidos_aprovados=Count('usuario__pedido', filter=Q(
            usuario__pedido__status='A', usuario__pedido__data__range=(data_inicio, data_fim))),
        total_pedidos_aprovados=Sum(
            Case(
                When(usuario__pedido__status='A', usuario__pedido__data__range=(
                    data_inicio, data_fim), then='usuario__pedido__total'),
                default=0,
                output_field=IntegerField()
            )
        ),
        modalidade_pedido=F('usuario__pedido__itempedido__produto_modalidade')
    ).order_by('-num_pedidos_aprovados')

    context = {
        'perfis_pedidos_aprovados': perfis_pedidos_aprovados,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }

    return render(request, 'gestao/clientes_que_mais_compram.html', context)


@login_required
def PerfilDetalheView(request, perfil_id, tipo_venda=None):
    perfil = get_object_or_404(Perfil, pk=perfil_id)
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    context = {
        'perfil': perfil,
        'tipo_venda': tipo_venda,
        'total_varejo': 0,
        'total_atacado': 0,
        'quantidade_varejo': 0,
        'quantidade_atacado': 0,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    if tipo_venda == 'V':  # Vendas no Varejo
        itens_pedido = ItemPedido.objects.filter(
            pedido__usuario=perfil.usuario, pedido__status='A', produto_modalidade='V')

        pedidos_aprovados = Pedido.objects.filter(status='A')

        if data_inicio and data_fim:
            pedidos_aprovados = pedidos_aprovados.filter(
                data__range=(data_inicio, data_fim))

        itens_pedido = itens_pedido.filter(pedido__in=pedidos_aprovados)

        total_varejo = sum(
            item_pedido.preco_promocional or item_pedido.preco for item_pedido in itens_pedido)
        quantidade_varejo = sum(
            item_pedido.quantidade for item_pedido in itens_pedido)

        context['itens_pedido'] = itens_pedido
        context['total_varejo'] = total_varejo
        context['quantidade_varejo'] = quantidade_varejo

    elif tipo_venda == 'A':  # Vendas no Atacado
        itens_pedido = ItemPedido.objects.filter(
            pedido__usuario=perfil.usuario, pedido__status='A', produto_modalidade='A')

        pedidos_aprovados = Pedido.objects.filter(status='A')

        if data_inicio and data_fim:
            pedidos_aprovados = pedidos_aprovados.filter(
                data__range=(data_inicio, data_fim))

        itens_pedido = itens_pedido.filter(pedido__in=pedidos_aprovados)

        total_atacado = sum(
            item_pedido.preco_promocional or item_pedido.preco for item_pedido in itens_pedido)
        quantidade_atacado = sum(
            item_pedido.quantidade for item_pedido in itens_pedido)

        context['itens_pedido'] = itens_pedido
        context['total_atacado'] = total_atacado
        context['quantidade_atacado'] = quantidade_atacado

    return render(request, 'gestao/perfil_detalhe.html', context)


@login_required
def TopVendedorView(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    pedidos_aprovados = Pedido.objects.filter(status='A')
    # Aplicar filtro de datas, se fornecidas
    if data_inicio and data_fim:
        pedidos_aprovados = pedidos_aprovados.filter(
            data__range=(data_inicio, data_fim))

    vendedores_pedidos_aprovados = Vendedor.objects.annotate(num_pedidos_aprovados=Count('pedido', filter=Q(
        pedido__status='A', pedido__data__range=(data_inicio, data_fim)))).order_by('-num_pedidos_aprovados')[:10]

    context = {
        'vendedores_pedidos_aprovados': vendedores_pedidos_aprovados,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }

    return render(request, 'gestao/vendedores_que_mais_vendem.html', context)


@login_required
def VendasGeraisView(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    pedidos_aprovados = Pedido.objects.filter(status='A')
    devolucoes = Devolucao.objects.all()

    # Aplicar filtro de datas, se fornecidas
    if data_inicio and data_fim:
        pedidos_aprovados = pedidos_aprovados.filter(
            data__range=(data_inicio, data_fim))

    quantidade_aprovados = pedidos_aprovados.count()
    quantidade_itens_aprovados = pedidos_aprovados.aggregate(
        total_itens=Sum('qtd_total'))['total_itens'] or 0
    total_pedidos = pedidos_aprovados.aggregate(total_pedidos=Sum('total'))[
        'total_pedidos'] or 0
    quantidade_devolucoes = devolucoes.count()
    soma_devolucoes = devolucoes.aggregate(total_devolucoes=Sum('pedido__total'))[
        'total_devolucoes'] or 0

    context = {
        'quantidade_aprovados': quantidade_aprovados,
        'quantidade_itens_aprovados': quantidade_itens_aprovados,
        'total_pedidos': total_pedidos,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'quantidade_devolucoes': quantidade_devolucoes,
        'soma_devolucoes': soma_devolucoes,
    }

    return render(request, 'gestao/vendas_gerais.html', context)


class RelatorioCaixaPorDataView(View):
    def get(self, request):
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')

        # Converter as datas para o formato correto (dd/mm/yyyy)
        data_inicio = datetime.strptime(
            data_inicio, '%d/%m/%Y').date() if data_inicio else None
        data_fim = datetime.strptime(
            data_fim, '%d/%m/%Y').date() if data_fim else None

        pedidos_aprovados = Pedido.objects.filter(status='A')
        devolucoes = Devolucao.objects.filter(pedido__in=pedidos_aprovados)

        # Aplicar filtro de datas, se fornecidas
        if data_inicio and data_fim:
            pedidos_aprovados = pedidos_aprovados.filter(
                data__range=(data_inicio, data_fim))
            devolucoes = devolucoes.filter(
                pedido__data__range=(data_inicio, data_fim))

        soma_quantidade_pedidos_c = pedidos_aprovados.filter(
            pagamento='C').count()
        soma_quantidade_pedidos_d = pedidos_aprovados.filter(
            pagamento='D').count()

        fiados_p = Fiado.objects.filter(
            data_p__range=(data_inicio, data_fim), status='P')
        soma_fiados = fiados_p.aggregate(soma=Sum('valor'))['soma'] or 0

        fiados_d = Fiado.objects.filter(
            data__range=(data_inicio, data_fim), status='D')
        diminuicao_fiados = - \
            (fiados_d.aggregate(soma=Sum('valor'))['soma'] or 0)

        total_pedidos = pedidos_aprovados.aggregate(
            total=Sum('total'))['total'] or 0
        valor_medio_vendas = pedidos_aprovados.aggregate(media=Avg('total'))[
            'media']
        soma_devolucoes = devolucoes.aggregate(
            soma=Sum('pedido__total'))['soma'] or 0

        soma_retiradas = Retirada.objects.filter(data__range=(
            data_inicio, data_fim)).aggregate(soma=Sum('retirada'))['soma'] or 0
        obs_retiradas = Retirada.objects.filter(data__range=(
            data_inicio, data_fim)).values_list('observacao', flat=True)

        soma_reforcos = Reforço.objects.filter(data__range=(
            data_inicio, data_fim)).aggregate(soma=Sum('reforço'))['soma'] or 0

        saldo = total_pedidos - soma_devolucoes + \
            soma_reforcos + soma_fiados - soma_retiradas + diminuicao_fiados

        context = {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'quantidade_pedidos_c': soma_quantidade_pedidos_c,
            'soma_quantidade_pedidos_c': soma_quantidade_pedidos_c,
            'quantidade_pedidos_d': soma_quantidade_pedidos_d,
            'soma_quantidade_pedidos_d': soma_quantidade_pedidos_d,
            'soma_fiados': soma_fiados,
            'diminuicao_fiados': diminuicao_fiados,
            'saldo': saldo,
            'data_caixa': data_inicio,
            'pedidos_aprovados': pedidos_aprovados,
            'quantidade_aprovados': pedidos_aprovados.count(),
            'devolucoes': devolucoes,
            'total_pedidos': total_pedidos,
            'valor_medio_vendas': valor_medio_vendas,
            'soma_devolucoes': soma_devolucoes,
            'reforco_form': ReforçoForm(),
            'retirada_form': RetiradaForm(),
            'soma_retiradas': soma_retiradas,
            'soma_reforcos': soma_reforcos,
            'obs_retiradas': obs_retiradas
        }

        return render(request, 'gestao/relatorio_caixa_por_data.html', context)


class DetalheCaixa(LoginRequiredMixin, TemplateView):
    template_name = 'gestao/detalhe_caixa.html'


class CaixaAbertoDetail(LoginRequiredMixin, DetailView):
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

        fiados = Fiado.objects.filter(data_p=data_caixa, status='P')
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

        obs_retiradas = Retirada.objects.filter(
            data=data_caixa).values_list('observacao', flat=True)

        soma_reforcos = Reforço.objects.filter(
            data=data_caixa).aggregate(soma=Sum('reforço'))['soma'] or 0

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
        context['obs_retiradas'] = obs_retiradas

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


@login_required
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


@login_required
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


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class Caixa(LoginRequiredMixin, CreateView):
    model = CaixaAberto
    form_class = CaixaAbertoForm
    template_name = 'gestao/caixa_create.html'
    success_url = reverse_lazy('gestao:lista_caixa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Controle de Caixa'
        return context


class CaixaAbertoListView(LoginRequiredMixin, ListView):
    model = CaixaAberto
    context_object_name = 'caixas'
    template_name = 'gestao/lista_caixa.html'
    paginate_by = 10
    ordering = ['-id']


class CaixaUpdateView(LoginRequiredMixin, UpdateView):
    model = CaixaAberto
    form_class = CaixaAbertoForm
    template_name = 'gestao/caixa_create.html'
    success_url = reverse_lazy('gestao:lista_caixa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Caixa'
        return context


class CaixaDeleteView(LoginRequiredMixin, DeleteView):
    model = CaixaAberto
    template_name = 'caixa_delete.html'
    success_url = reverse_lazy('gestao:lista_caixa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Caixa?'
        return context


def buscar_caixa_aberto(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = CaixaAberto.objects.filter(Q(nome__icontains=query))

    return render(request, 'gestao/lista_caixa.html', {'caixas': resultados})
