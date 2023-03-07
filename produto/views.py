from django.urls import reverse_lazy
from .models import Produto
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import DeleteView, CreateView
from django.forms.models import modelformset_factory

from produto.forms import CategoriaForm, ProdutoForm

from . import models
from perfil.models import Perfil
from .models import Categoria, Variacao, ImagemProduto, Produto


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = models.Categoria.objects.all()
        return context


class ListaProdutosPorCategoria(ListView):
    model = models.Produto
    template_name = 'produto/lista_por_categoria.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']

    def get_queryset(self):
        categoria_slug = self.kwargs['categoria_slug']
        categoria = get_object_or_404(models.Categoria, slug=categoria_slug)
        return models.Produto.objects.filter(categoria=categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_slug = self.kwargs['categoria_slug']
        categoria = get_object_or_404(models.Categoria, slug=categoria_slug)
        context['categoria'] = categoria
        context['categorias'] = models.Categoria.objects.all()
        return context


class produto_add(CreateView):
    template_name = 'produto_add.html'
    model = Produto
    fields = ['nome', 'descricao_curta',
              'descricao_longa', 'imagem', 'preco_marketing', 'preco_marketing_promocional', 'tipo', 'categoria']
    success_url = reverse_lazy('produto:categoria_add')

    def form_valid(self, form):
        form.instance.user = self.request.user
        produto = form.save()

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
        # obtém os dados das imagens enviadas pelo formulário
        imagens = self.request.FILES.getlist('imagem_produto')
        for imagem in imagens:
            imagem_produto = ImagemProduto(
                produto=produto,
                imagem=imagem
            )
            imagem_produto.save()

        # obtém os dados das imagens enviadas pelo formulário via formset
        imagem_formset = modelformset_factory(
            ImagemProduto, fields=('imagem',), extra=3)(self.request.POST, self.request.FILES)
        if imagem_formset.is_valid():
            imagens = imagem_formset.save(commit=False)
            for imagem in imagens:
                imagem.produto = produto
                imagem.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].enctype = 'multipart/form-data'
        context['categorias'] = Categoria.objects.all()
        ImagemFormSet = modelformset_factory(
            ImagemProduto, fields=('imagem',), extra=3)
        context['imagem_formset'] = ImagemFormSet(
            queryset=ImagemProduto.objects.none())
        return context


def produto_edit(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('produto:categoria_add')
    context = {
        'form': form,
        'produto': produto,
    }

    return render(request, 'categoria_add.html', context)


class produto_delete(DeleteView):
    model = Produto
    success_url = reverse_lazy('produto:categoria_add')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Produto, slug=self.kwargs.get('slug'))
        return obj


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


def categoria_list(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'categoria_add.html', context)


def categoria_add(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    form = CategoriaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('produto:categoria_add')
    context = {'form': form, 'categorias': categorias, 'produtos': produtos}
    return render(request, 'categoria_add.html', context)


def categoria_edit(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('categoria:categoria_add')
    context = {
        'form': form,
        'categoria': categoria,
    }

    return render(request, 'categoria_add.html', context)


class categoria_delete(DeleteView):
    model = Categoria
    success_url = reverse_lazy('produto:categoria_add')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Categoria, slug=slug)
        return obj


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo ']
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


class AdicionarAoCarrinho(View):
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


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
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

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }

        return render(self.request, 'produto/resumodacompra.html', contexto)
