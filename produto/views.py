from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from pedido.forms import CupomForm

from pedido.models import Cupom
import utils
from utils.utils import cart_totals

from .models import Influenciadores, Produto
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.forms.models import modelformset_factory

from produto.forms import CategoriaForm, InfluenciadoresForm, ProdutoForm, TipoForm, VariacaoForm, FornecedorForm, ContasPagarForm
from django.views.generic import TemplateView
from . import models
from perfil.models import Perfil
from .models import Categoria, Variacao, ImagemProduto, Produto, Fornecedor, ContasPagar, Tipo


class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedor_create.html'
    success_url = reverse_lazy('produto:lista_fornecedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Fornecedor'
        return context


class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    context_object_name = 'fornecedores'
    template_name = 'produto/lista_fornecedores.html'
    paginate_by = 10
    ordering = ['-id']


class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedor_create.html'
    success_url = reverse_lazy('produto:lista_fornecedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Fornecedor'
        return context


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'fornecedor_delete.html'
    success_url = reverse_lazy('produto:lista_fornecedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Fornecedor'
        return context


class ContasView(LoginRequiredMixin, TemplateView):
    template_name = 'contas.html'


class ContasPagarCreateView(LoginRequiredMixin, CreateView):
    model = ContasPagar
    form_class = ContasPagarForm
    template_name = 'contaspagar_create.html'
    success_url = reverse_lazy('produto:lista_contaspagar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Conta a Pagar'
        return context


class ContasPagarListView(LoginRequiredMixin, ListView):
    model = ContasPagar
    context_object_name = 'contaspagar'
    template_name = 'produto/lista_contaspagar.html'
    paginate_by = 10
    ordering = ['-id']


class ContasPagarUpdateView(LoginRequiredMixin, UpdateView):
    model = ContasPagar
    form_class = ContasPagarForm
    template_name = 'contaspagar_create.html'
    success_url = reverse_lazy('produto:lista_contaspagar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Conta a Pagar'
        return context


class ContasPagarDeleteView(LoginRequiredMixin, DeleteView):
    model = ContasPagar
    template_name = 'contaspagar_delete.html'
    success_url = reverse_lazy('produto:lista_contaspagar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Conta a Pagar'
        return context


class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista_varejo.html'
    context_object_name = 'produtos'
    paginate_by = 12
    ordering = ['-destaque', '-id']

    def get_queryset(self):
        nomes_produtos = Produto.objects.values_list(
            'nome', flat=True).distinct()
        queryset = Produto.objects.filter(
            nome__in=nomes_produtos, is_primary=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = models.Categoria.objects.all()
        context['tipos'] = models.Tipo.objects.all()
        return context


class ListaProdutosPorTipo(ListView):
    model = models.Produto
    template_name = 'produto/lista_por_tipo.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-destaque', '-id']

    def get_queryset(self):
        tipo_slug = self.kwargs['tipo_slug']
        tipo = get_object_or_404(models.Tipo, slug=tipo_slug)
        return models.Produto.objects.filter(tipo=tipo)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_slug = self.kwargs['tipo_slug']
        tipo = get_object_or_404(models.Tipo, slug=tipo_slug)
        context['tipo'] = tipo
        context['tipos'] = models.Tipo.objects.all()
        context['categorias'] = models.Categoria.objects.all()

        return context


class ListaProdutosPorTipoAtacado(ListView):
    model = models.Produto
    template_name = 'produto/lista_por_tipo_atacado.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-destaque', '-id']

    def get_queryset(self):
        tipoatacado_slug = self.kwargs['tipoatacado_slug']
        tipoatacado = get_object_or_404(models.Tipo, slug=tipoatacado_slug)
        return models.Produto.objects.filter(tipo=tipoatacado)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipoatacado_slug = self.kwargs['tipoatacado_slug']
        tipoatacado = get_object_or_404(models.Tipo, slug=tipoatacado_slug)
        context['tipoatacado'] = tipoatacado
        context['tiposatacados'] = models.Tipo.objects.all()
        context['categoriasatacados'] = models.Categoria.objects.all()

        return context


class ListaProdutosPorCategoria(ListView):
    model = models.Produto
    template_name = 'produto/lista_por_categoria.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-destaque', '-id']

    def get_queryset(self):
        categoria_slug = self.kwargs['categoria_slug']
        categoria = get_object_or_404(models.Categoria, slug=categoria_slug)
        return models.Produto.objects.filter(categoria=categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_slug = self.kwargs['categoria_slug']
        categoria = get_object_or_404(models.Categoria, slug=categoria_slug)
        context['categoria'] = categoria
        context['tipos'] = models.Tipo.objects.all()

        context['categorias'] = models.Categoria.objects.all()
        return context


class ListaProdutosPorCategoriaAtacado(ListView):
    model = models.Produto
    template_name = 'produto/lista_por_categoria_atacado.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-destaque', '-id']

    def get_queryset(self):
        categoriaatacado_slug = self.kwargs['categoriaatacado_slug']
        categoriaatacado = get_object_or_404(
            models.Categoria, slug=categoriaatacado_slug)
        return models.Produto.objects.filter(categoria=categoriaatacado)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoriaatacado_slug = self.kwargs['categoriaatacado_slug']
        categoriaatacado = get_object_or_404(
            models.Categoria, slug=categoriaatacado_slug)
        context['categoriaatacado'] = categoriaatacado
        context['tiposatacados'] = models.Tipo.objects.all()
        context['categoriasatacados'] = models.Categoria.objects.all()
        return context


class TipoCreateView(LoginRequiredMixin, CreateView):
    model = Tipo
    form_class = TipoForm
    template_name = 'tipo_create.html'
    success_url = reverse_lazy('produto:categoria_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipo do Produto'
        # Adiciona o form de cadastro de tipos ao contexto
        context['tipo_form'] = self.form_class()

        return context


class TipoUpdateView(LoginRequiredMixin, UpdateView):
    model = Tipo
    form_class = TipoForm
    template_name = 'tipo_create.html'
    success_url = reverse_lazy('produto:categoria_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo'
        return context


class TipoDeleteView(LoginRequiredMixin, DeleteView):
    model = Tipo
    template_name = 'tipo_delete.html'
    success_url = reverse_lazy('produto:categoria_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Tipo'
        return context


class produto_add(LoginRequiredMixin, CreateView):
    template_name = 'produto_add.html'
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('produto:categoria_add')
    ImagemProdutoFormSet = inlineformset_factory(
        Produto, ImagemProduto, fields=('imagem',), extra=3)

    def form_valid(self, form):
        form.instance.user = self.request.user
        produto = form.save(commit=False)
        produto.save()

        imagem_formset = self.ImagemProdutoFormSet(
            self.request.POST, self.request.FILES, instance=produto)

        if imagem_formset.is_valid():
            imagem_formset.save()

        nome_variacao = self.request.POST.getlist('nome_variacao[]')
        preco_variacao = self.request.POST.getlist('preco_variacao[]')
        preco_promocional_variacao = self.request.POST.getlist(
            'preco_promocional_variacao[]')
        estoque_variacao = self.request.POST.getlist('estoque_variacao[]')

        for i in range(len(nome_variacao)):
            variacao = Variacao(
                produto=produto,
                nome=nome_variacao[i],
                preco=preco_variacao[i],
                preco_promocional=preco_promocional_variacao[i] or None,
                estoque=estoque_variacao[i],
            )
            variacao.save()

        return redirect('produto:categoria_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['variacao'] = Variacao.objects.all()
        context['imagem_formset'] = self.ImagemProdutoFormSet(
            queryset=ImagemProduto.objects.none())
        return context


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produto_update.html'
    success_url = reverse_lazy('produto:categoria_add')
    ImagemProdutoFormSet = inlineformset_factory(
        Produto, ImagemProduto, fields=('imagem',), extra=3)

    def form_valid(self, form):
        form.instance.user = self.request.user
        produto = form.save(commit=False)
        produto.save()

        imagem_formset = self.ImagemProdutoFormSet(
            self.request.POST, self.request.FILES, instance=produto)

        if imagem_formset.is_valid():
            imagem_formset.save()

        nome_variacao = self.request.POST.getlist('nome_variacao[]')
        preco_variacao = self.request.POST.getlist('preco[]')
        preco_promocional_variacao = self.request.POST.getlist(
            'preco_promocional[]')
        estoque_variacao = self.request.POST.getlist('estoque_variacao[]')
        excluir_variacao_ids = self.request.POST.getlist(
            'excluir_variacao_id[]')

        for i in range(len(nome_variacao)):
            variacao_id = self.request.POST.getlist('variacao_id[]')[i]

            if variacao_id in excluir_variacao_ids:
                Variacao.objects.filter(id=variacao_id).delete()
                continue

            if variacao_id:
                variacao = Variacao.objects.get(id=variacao_id)
                variacao.nome = nome_variacao[i]
                variacao.preco = preco_variacao[i].replace(
                    ',', '.')  # Substituir vírgula por ponto
                variacao.preco_promocional = preco_promocional_variacao[i].replace(
                    ',', '.') or None  # Substituir vírgula por ponto
                variacao.estoque = estoque_variacao[i]
                variacao.save()
            else:
                variacao = Variacao.objects.create(
                    produto=produto,
                    nome=nome_variacao[i],
                    # Substituir vírgula por ponto
                    preco=preco_variacao[i].replace(',', '.'),
                    preco_promocional=preco_promocional_variacao[i].replace(
                        ',', '.') or None,  # Substituir vírgula por ponto
                    estoque=estoque_variacao[i]
                )

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['imagem_formset'] = self.ImagemProdutoFormSet(
            queryset=ImagemProduto.objects.none())

        produto = self.get_object()
        context['variacoes'] = Variacao.objects.filter(produto=produto)

        return context


class EstoqueVariacaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        produto_id = kwargs.get('produto_id')
        produto = Produto.objects.get(id=produto_id)
        variacoes = Variacao.objects.filter(produto=produto)
        context = {
            'produto': produto,
            'variacoes': variacoes,
        }
        return render(request, 'estoque_variacao.html', context)


@login_required
def GestaoEstoqueVariacao(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()

    form = VariacaoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('produto:estoque_variacao')
    context = {'form': form, 'categorias': categorias,
               'produtos': produtos, }
    return render(request, 'gestao_estoque.html', context)


@login_required
def variacao_add(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()

    form = VariacaoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('produto:estoque_variacao')
    context = {'form': form, 'categorias': categorias,
               'produtos': produtos, }
    return render(request, 'variacao_add.html', context)


@login_required
def variacao_edit(request, id):
    variacao = get_object_or_404(Variacao, id=id)
    form = VariacaoForm(request.POST or None, instance=variacao)
    if form.is_valid():
        form.save()
        return redirect('produto:estoque_variacao', produto_id=variacao.produto.id)

    context = {
        'form': form,
        'variacao': variacao,
    }
    return render(request, 'variacao_add.html', context)


class VariacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Variacao
    template_name = 'variacao_delete.html'
    success_url = reverse_lazy('produto:gestao_estoque')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Variação'
        return context


class produto_delete(LoginRequiredMixin, DeleteView):
    model = Produto
    success_url = reverse_lazy('produto:categoria_add')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Produto, slug=self.kwargs.get('slug'))
        return obj


class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto = self.get_object()
        produtos_iguais = Produto.objects.filter(
            nome=produto.nome)
        context['produtos_iguais'] = produtos_iguais
        return context


class DetalheProduto2(DetailView):
    model = models.Produto
    template_name = 'pedido/detalhe_produto_admin.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = models.Categoria.objects.all()
        return context


@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'categoria_add.html', context)


@login_required
def categoria_add(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    tipos = Tipo.objects.all()

    form = CategoriaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('produto:categoria_add')
    context = {'form': form, 'categorias': categorias,
               'produtos': produtos, 'tipos': tipos}
    return render(request, 'categoria_add.html', context)


@login_required
def categoria_edit(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('produto:categoria_add')
    context = {
        'form': form,
        'categoria': categoria,
    }

    return render(request, 'categoria_add.html', context)


class categoria_delete(LoginRequiredMixin, DeleteView):
    model = Categoria
    success_url = reverse_lazy('produto:categoria_add')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Categoria, slug=slug)
        return obj


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get(
            'termo') or self.request.session.get('termo')
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        self.request.session.save()
        return qs


def buscar_produto(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Produto.objects.filter(Q(nome__icontains=query))

    return render(request, 'gestao_estoque.html', {'produtos': resultados})


def buscar_conta_pagar(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = ContasPagar.objects.filter(
            Q(fornecedor__nome__icontains=query))

    return render(request, 'produto/lista_contaspagar.html', {'contaspagar': resultados})


def buscar_fornecedores(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Fornecedor.objects.filter(
            Q(nome__icontains=query))

    return render(request, 'produto/lista_fornecedores.html', {'fornecedores': resultados})


class AdicionarAoCarrinho(View):
    def get(self, request, *args, **kwargs):
        http_referer = request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = request.GET.get('vid')
        quantidade = int(request.GET.get('quantidade', 1))

        if not variacao_id:
            messages.error(
                request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto
        produto_modalidade = produto.modalidade
        produto_cor = produto.cor
        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional

        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if quantidade > variacao_estoque:
            messages.error(
                request,
                f'Estoque insuficiente. A quantidade máxima disponível é {variacao_estoque}.'
            )
            return redirect(http_referer)

        if not request.session.get('carrinho'):
            request.session['carrinho'] = {}
            request.session.save()

        carrinho = request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += quantidade

            if quantidade_carrinho > variacao_estoque:
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'produto_modalidade': produto_modalidade,
                'produto_cor': produto_cor,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario * quantidade,
                'preco_quantitativo_promocional': preco_unitario_promocional * quantidade,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }

        request.session.save()

        messages.success(
            request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)


class AdicionarAoCarrinhoAdmin(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')
        int(variacao_id)

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, request, *args, **kwargs):
        variacao_id = self.request.GET.get('vid')
        carrinho = request.session.get('carrinho')

        if not carrinho or not carrinho.get(variacao_id):
            return redirect('produto:lista')

        produto_id = carrinho[variacao_id]['produto_id']

        if carrinho[variacao_id]['quantidade'] > 1:
            carrinho[variacao_id]['quantidade'] -= 1
            carrinho[variacao_id]['preco_quantitativo'] -= carrinho[variacao_id]['preco_unitario']
            carrinho[variacao_id]['preco_quantitativo_promocional'] -= carrinho[variacao_id]['preco_unitario_promocional']
        else:
            del carrinho[variacao_id]

        request.session['carrinho'] = carrinho
        messages.success(
            request,
            f'Produto removido do carrinho com sucesso.'
        )

        return redirect('produto:carrinho')


class RemoverDoCarrinhoAdmin(View):
    def get(self, request, *args, **kwargs):
        variacao_id = self.request.GET.get('vid')
        carrinho = request.session.get('carrinho')

        if not carrinho or not carrinho.get(variacao_id):
            return redirect('produto:lista')

        produto_id = carrinho[variacao_id]['produto_id']

        if carrinho[variacao_id]['quantidade'] > 1:
            carrinho[variacao_id]['quantidade'] -= 1
            carrinho[variacao_id]['preco_quantitativo'] -= carrinho[variacao_id]['preco_unitario']
            carrinho[variacao_id]['preco_quantitativo_promocional'] -= carrinho[variacao_id]['preco_unitario_promocional']
        else:
            del carrinho[variacao_id]

        request.session['carrinho'] = carrinho
        messages.success(
            request,
            f'Produto removido do carrinho com sucesso.'
        )

        return redirect('produto:carrinho_admin')


class Carrinho(View):
    def get(self, *args, **kwargs):
        cupom_codigo = self.request.GET.get('cupom', None)
        cupom = None

        if cupom_codigo:
            try:
                cupom = Cupom.objects.get(codigo=cupom_codigo)
            except Cupom.DoesNotExist:
                pass

        carrinho = self.request.session.get('carrinho', {})
        # Passando o cupom para a função cart_totals
        totals = cart_totals(carrinho, cupom)

        contexto = {
            'carrinho': carrinho,
            'cupons': Cupom.objects.all(),
            'cupom_aplicado': cupom,
            'cart_totals': totals
        }

        return render(self.request, 'produto/carrinho.html', contexto)


class CarrinhoAdmin(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {}),
            'cupom_form': CupomForm()  # Passa o formulário de cupom para o template
        }

        return render(self.request, 'produto/carrinho.html', contexto)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho', {})
        cupom_codigo = self.request.GET.get('cupom', None)
        cupom = Cupom.objects.get(
            codigo=cupom_codigo) if cupom_codigo else None
        # Chamando a função cart_totals com o cupom aplicado
        totals = cart_totals(carrinho, cupom)
        self.request.session['totals'] = totals
        self.request.session.modified = True

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
            'cart_totals': totals
        }

        return render(self.request, 'produto/resumodacompra.html', contexto)


class ResumoDaCompraAdmin(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }

        return render(self.request, 'pedido/resumodacompra_admin.html', contexto)


class InfluenciadoresCreateView(LoginRequiredMixin, CreateView):
    model = Influenciadores
    form_class = InfluenciadoresForm
    template_name = 'influenciadores_create.html'
    success_url = reverse_lazy('produto:lista_influenciadores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Influenciadores'
        return context


class InfluenciadoresListView(LoginRequiredMixin, ListView):
    model = Influenciadores
    context_object_name = 'influenciadores'
    template_name = 'produto/lista_influenciadores.html'
    paginate_by = 10
    ordering = ['-id']


class InfluenciadoresUpdateView(LoginRequiredMixin, UpdateView):
    model = Influenciadores
    form_class = InfluenciadoresForm
    template_name = 'influenciadores_create.html'
    success_url = reverse_lazy('produto:lista_influenciadores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Envio'
        return context


class InfluenciadoresDeleteView(LoginRequiredMixin, DeleteView):
    model = Influenciadores
    template_name = 'influenciadores_delete.html'
    success_url = reverse_lazy('produto:lista_influenciadores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Envio'
        return context
