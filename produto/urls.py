from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import categoria_delete, produto_delete, EstoqueVariacaoView, CadastrosView, FornecedorCreateView
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name="lista"),
    path('<slug>', views.DetalheProduto.as_view(), name="detalhe"),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(),
         name="adicionaraocarrinho"),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(),
         name="removerdocarrinho"),
    path('carrinho/', views.Carrinho.as_view(), name="carrinho"),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name="resumodacompra"),
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
    path('novo_fornecedor/', FornecedorCreateView.as_view(),
         name='fornecedor_create'),




















]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
