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

from datetime import date, datetime
from django.db.models import Sum, Avg, Count, F
from django.db.models import Q

from vendas.models import Vendedor


class RelatorioView(TemplateView):
    template_name = 'relatorio.html'


def TopProdutosView(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converter as datas para o formato correto (dd/mm/yyyy)
    data_inicio = datetime.strptime(
        data_inicio, '%d/%m/%Y').date() if data_inicio else None
    data_fim = datetime.strptime(
        data_fim, '%d/%m/%Y').date() if data_fim else None

    itens_aprovados = ItemPedido.objects.filter(pedido__status='A')

    # Aplicar filtro de datas, se fornecidas
    if data_inicio and data_fim:
        itens_aprovados = itens_aprovados.filter(
            pedido__data__range=(data_inicio, data_fim))

    produtos_quantidades = (
        itens_aprovados
        .values('produto', 'produto_id')
        .annotate(quantidade=Sum('quantidade'))
        .order_by('-quantidade')[:10]
    )

    context = {
        'produtos_quantidades': produtos_quantidades,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(request, 'gestao/produtos_mais_vendidos.html', context)


def TopTodosProdutosView(request):
    itens_aprovados = ItemPedido.objects.filter(pedido__status='A')

    produtos_quantidades = (
        itens_aprovados
        .values('produto', 'produto_id')
        .annotate(quantidade=Sum('quantidade'))
        .order_by('-quantidade')
    )

    context = {
        'produtos_quantidades': produtos_quantidades,
    }

    return render(request, 'gestao/todos_os_produtos_vendas.html', context)


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

    perfis_pedidos_aprovados = Perfil.objects.annotate(num_pedidos_aprovados=Count('usuario__pedido', filter=Q(
        usuario__pedido__status='A', usuario__pedido__data__range=(data_inicio, data_fim)))).order_by('-num_pedidos_aprovados')[:10]

    context = {
        'perfis_pedidos_aprovados': perfis_pedidos_aprovados,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }

    return render(request, 'gestao/clientes_que_mais_compram.html', context)


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
    success_url = reverse_lazy('gestao:lista_caixa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Controle de Caixa'
        return context


class CaixaAbertoListView(ListView):
    model = CaixaAberto
    context_object_name = 'caixas'
    template_name = 'gestao/lista_caixa.html'
    paginate_by = 10
    ordering = ['-id']


class CaixaUpdateView(UpdateView):
    model = CaixaAberto
    form_class = CaixaAbertoForm
    template_name = 'gestao/caixa_create.html'
    success_url = reverse_lazy('gestao:lista_caixa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Caixa'
        return context


class CaixaDeleteView(DeleteView):
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
