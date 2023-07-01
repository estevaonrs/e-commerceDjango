

def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])


def cart_totals(carrinho, cupom=None):
    sub_total = sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )

    if cupom and cupom.valor > 0:
        desconto = sub_total * (cupom.valor / 100)
        sub_total -= desconto

    return sub_total
