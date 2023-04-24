from django.views.generic import ListView
from django.shortcuts import render
from django.views.generic import TemplateView


from pedido.models import Devolucao


class GestaoView(TemplateView):
    template_name = 'gestao.html'


class ListaDevolucao(ListView):
    model = Devolucao
    context_object_name = 'devolucoes'
    template_name = 'gestao/lista_devolucao.html'
    paginate_by = 10
    ordering = ['-id']
