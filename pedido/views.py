# from django.http import HttpResponse
from django.dispatch import receiver
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.db.models.signals import pre_delete
from produto.models import Variacao
from utils import utils
from produto import models
from .models import Cupom, Devolucao, ItemPedido, Pedido
from pedido.forms import CupomForm, DevolucaoForm, PagamentoForm, PedidoForm
from django.views.generic.edit import CreateView
from django.db.models import Prefetch
from .models import ItemPedido
from asaas.payments import CreditCard, CreditCardHolderInfo, BillingType
from datetime import date
from asaas import Asaas, Customer
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class DevolucaoCreateView(LoginRequiredMixin, CreateView):
    model = Devolucao
    form_class = DevolucaoForm
    template_name = 'devolucao_create.html'
    success_url = reverse_lazy('pedido:lista_devolucao')
    # Substitua 'nome_da_url_de_login' pela URL real da página de login
    login_url = reverse_lazy('perfil:criar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Devolução'
        return context


class DevolucaoListView(LoginRequiredMixin, ListView):
    model = Devolucao
    context_object_name = 'devolucoes'
    template_name = 'pedido/lista_devolucao.html'
    paginate_by = 10
    ordering = ['-id']


class DevolucaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Devolucao
    form_class = DevolucaoForm
    template_name = 'devolucao_create.html'
    success_url = reverse_lazy('pedido:lista_devolucao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Devolução'
        return context


class DevolucaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Devolucao
    template_name = 'devolucao_delete.html'
    success_url = reverse_lazy('pedido:lista_devolucao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Devolução?'
        return context


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


@login_required
def pagar(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            nome_cliente = form.cleaned_data['nome_cliente']
            cpf_cnpj = form.cleaned_data['cpf_cnpj']
            numero_cartao = form.cleaned_data['numero_cartao']
            mes_validade = form.cleaned_data['mes_validade']
            ano_validade = form.cleaned_data['ano_validade']
            ccv = form.cleaned_data['ccv']
            email = form.cleaned_data['email']
            endereco = form.cleaned_data['endereco']
            cep = form.cleaned_data['cep']
            telefone = form.cleaned_data['telefone']

            # Create an instance of the Asaas library
            asaas = Asaas(access_token='$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNTY3MzI6OiRhYWNoXzMzMzAzZDY2LTA3YTUtNDJhNi1iYzRjLTAwYzNkYjEwOWI0MA==', production=False)

            # Verify if the customer already exists based on CPF/CNPJ
            existing_customers = asaas.customers.list(cpfCnpj=cpf_cnpj)

            if len(existing_customers) > 0:
                # Customer already exists, use the existing customer ID
                customer_id = existing_customers[0].id
            else:
                # Create a new customer
                customer_id = None

            now = date.today()
            date_created = now.strftime("%Y-%m-%d")

            if customer_id is None:
                new_customer = asaas.customers.new(
                    name=nome_cliente,
                    email=email,
                    cpfCnpj=cpf_cnpj,
                    postalCode=cep,
                    addressNumber=endereco,
                    phone=telefone
                )
                customer_id = new_customer.id

            credit_card = CreditCard(
                holderName=nome_cliente,
                number=numero_cartao,
                expiryYear=ano_validade,
                expiryMonth=mes_validade,
                ccv=ccv
            )

            credit_card_holder_info = CreditCardHolderInfo(
                name=nome_cliente,
                email=email,
                cpfCnpj=cpf_cnpj,
                postalCode=cep,
                addressNumber=endereco,
                addressComplement='',
                phone=telefone
            )

            customer = Customer(
                id=customer_id,
                dateCreated=date_created,
                name=nome_cliente,
                cpfCnpj=cpf_cnpj
            )
            valor_plano = float(pedido.total)

            pagamento = asaas.payments.new(
                customer=customer,
                billingType=BillingType.CREDIT_CARD,
                value=valor_plano,
                dueDate=now,
                creditCard=credit_card.json(),
                creditCardHolderInfo=credit_card_holder_info.json()
            )

            if pagamento.id:
                mensagem = "Pagamento processado com sucesso!"
            else:
                mensagem = "Falha no processamento do pagamento. Por favor, tente novamente."

            # Redirecionamento para a página de sucesso (PRG pattern)
            return redirect(reverse('pedido:pedido_sucesso') + f'?mensagem={mensagem}')

    else:
        form = PagamentoForm()

    return render(request, 'pedido/pagar.html', {'form': form, 'pedido': pedido})


class SucessoView(LoginRequiredMixin, TemplateView):
    template_name = 'pedido/pedido_sucesso.html'


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        totals = self.request.session.get('totals')

        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns '\
                    'produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = totals  # Utiliza o valor de totals armazenado na sessão

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        # Adicione o código abaixo para salvar o cupom junto com o pedido
        cupom_codigo = self.request.GET.get('cupom')
        try:
            cupom = Cupom.objects.get(codigo=cupom_codigo)
        except Cupom.DoesNotExist:
            cupom = None

        if cupom:
            pedido.cupom = cupom

        pedido.save()
        # Fim do trecho adicionado

        for variacao in bd_variacoes:
            vid = str(variacao.id)
            qtd_carrinho = carrinho[vid]['quantidade']
            variacao.estoque -= qtd_carrinho
            variacao.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_modalidade=v['produto_modalidade'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']

        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'id': pedido.id
                }
            )
        )

    @transaction.atomic
    def atualizar_estoque_variacoes(carrinho):
        for item in carrinho:
            variacao = item.variacao
            variacao.estoque -= item.quantidade
            variacao.save()

    @receiver(pre_delete, sender=Pedido)
    def atualizar_estoque_variacoes(sender, instance, **kwargs):
        for item in instance.itempedido_set.all():
            try:
                variacao = Variacao.objects.get(id=item.variacao_id)
                variacao.estoque += item.quantidade
                variacao.save()
            except Variacao.DoesNotExist:
                # Lidar com a variação inexistente aqui (por exemplo, registrar um erro ou ignorar)
                pass


class SalvarPedidoAdmin(View):
    template_name = 'pedido/lista_admin.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('pedido:criar_novo_pedido')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns '\
                    'produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        pedido.save()

        for variacao in bd_variacoes:
            vid = str(variacao.id)
            qtd_carrinho = carrinho[vid]['quantidade']
            variacao.estoque -= qtd_carrinho
            variacao.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']

        return redirect(
            reverse(
                'pedido:lista_admin'

            )
        )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = models.Categoria.objects.all()
        return context


@login_required
def detalhe_admin(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        pedido.status = request.POST['status']
        pedido.save()

    return render(request, 'pedido/detalhe_admin.html', {'pedido': pedido})


@login_required
def excluir_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedido:lista_admin')

    return render(request, 'pedido/excluir_pedido.html', {'pedido': pedido})


class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido/pedido_status_create.html'
    success_url = reverse_lazy('pedido:lista_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Pedido'
        return context


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = models.Categoria.objects.all()
        return context


class lista_admin(LoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidosadmin'
    template_name = 'pedido/lista_admin.html'
    paginate_by = 10
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = models.Categoria.objects.all()
        return context


class criar_novo_pedido(LoginRequiredMixin, TemplateView):
    template_name = 'pedido/pedido_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = models.Produto.objects.all()
        return context


def buscar_pedido(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Pedido.objects.filter(Q(id__icontains=query))

    return render(request, 'pedido/lista_admin.html', {'pedidosadmin': resultados})


def buscar_devolucao(request):
    query = request.GET.get('q')
    resultados = None

    if query:
        resultados = Devolucao.objects.filter(
            Q(itens__pedido__id__icontains=query))

    return render(request, 'pedido/lista_devolucao.html', {'devolucoes': resultados})


class CupomCreateView(LoginRequiredMixin, CreateView):
    model = Cupom
    form_class = CupomForm
    template_name = 'cupom_create.html'
    success_url = reverse_lazy('pedido:lista_cupom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Devolução'
        return context


class CupomListView(LoginRequiredMixin, ListView):
    model = Cupom
    context_object_name = 'cupons'
    template_name = 'pedido/lista_cupom.html'
    paginate_by = 10
    ordering = ['-id']


class CupomUpdateView(LoginRequiredMixin, UpdateView):
    model = Cupom
    form_class = CupomForm
    template_name = 'cupom_create.html'
    success_url = reverse_lazy('pedido:lista_cupom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cupom'
        return context


class CupomDeleteView(LoginRequiredMixin, DeleteView):
    model = Cupom
    template_name = 'cupom_delete.html'
    success_url = reverse_lazy('pedido:lista_cupom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Cupom?'
        return context
