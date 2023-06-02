from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ContasPagarDeleteView, ContasPagarUpdateView, categoria_delete, produto_delete, EstoqueVariacaoView, CadastrosView, FornecedorCreateView, GestaoEstoqueVariacao, ContasView, ContasPagarCreateView
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name="lista"),
    path('<slug>', views.DetalheProduto.as_view(), name="detalhe"),
    path('detalhe_loja_admin/<slug>',
         views.DetalheProduto2.as_view(), name="detalhe_loja_admin"),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(),
         name="adicionaraocarrinho"),
    path('adicionaraocarrinho_admin/', views.AdicionarAoCarrinhoAdmin.as_view(),
         name="adicionaraocarrinho_admin"),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(),
         name="removerdocarrinho"),
    path('removerdocarrinho_admin/', views.RemoverDoCarrinhoAdmin.as_view(),
         name="removerdocarrinho_admin"),
    path('carrinho/', views.Carrinho.as_view(), name="carrinho"),
    path('carrinho_admin/', views.CarrinhoAdmin.as_view(), name="carrinho_admin"),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name="resumodacompra"),
    path('resumodacompra_admin/', views.ResumoDaCompraAdmin.as_view(),
         name="resumodacompra_admin"),
    path('busca/', views.Busca.as_view(), name="busca"),
    path('produto_add/', views.produto_add.as_view(), name="produto_add"),
    path('categoria/<slug:categoria_slug>/',
         views.ListaProdutosPorCategoria.as_view(), name='lista_por_categoria'),
    path('categoria_add/', views.categoria_add, name='categoria_add'),
    path('categoria/list/', views.categoria_list, name='categoria_list'),
    path('categoria_edit/<int:id>/', views.categoria_edit, name='categoria_edit'),
    path('<slug:slug>/excluir/', categoria_delete.as_view(),
         name='categoria_delete'),
    path('produto/<slug:slug>/excluir/', produto_delete.as_view(),
         name='produto_delete'),
    path('produto_edit/<int:id>/', views.produto_edit, name='produto_edit'),
    path('<int:produto_id>/estoque_variacao/',
         EstoqueVariacaoView.as_view(), name='estoque_variacao'),
    path('variacao/<int:id>/edit/', views.variacao_edit, name='variacao_edit'),
    path('variacao_add/', views.variacao_add, name='variacao_add'),
    path('cadastros/', CadastrosView.as_view(), name='cadastros'),
    path('contas/', ContasView.as_view(), name='contas'),
    path('novo_fornecedor/', FornecedorCreateView.as_view(),
         name='fornecedor_create'),
    path('conta_pagar/', ContasPagarCreateView.as_view(),
         name='conta_pagar'),
    path('GestaoEstoqueVariacao/', GestaoEstoqueVariacao,
         name='gestao_estoque'),
    path('lista_contaspagar/', views.ContasPagarListView.as_view(),
         name='lista_contaspagar'),
    path('conta_pagar_edit/<int:pk>/',
         ContasPagarUpdateView.as_view(), name='conta_pagar_edit'),
    path('conta_pagar_delete/<int:pk>/',
         ContasPagarDeleteView.as_view(), name='conta_pagar_delete'),






















]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
