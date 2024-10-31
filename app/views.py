from django.shortcuts import render
from django.views import View
from .models import (
    Categoria, Marca, Produto, Cliente, Venda, ItemVenda, Pagamento,
    EnderecoEntrega, Avaliacao, Comentario, Cupom, Carrinho, 
    ItemCarrinho, Desejo, ItemDesejo, Notificacao, Log
)


###############################################################################
# CONTROLADORES DA APLICAÇÃO (RESPONSÁVEIS POR GERENCIAR AS REQUISIÇÕES HTTP) #
###############################################################################


class IndexView(View):
    def get(self, request):
        return render(request, 'pages/index.html')
    
    def post(self, request):
        pass
    