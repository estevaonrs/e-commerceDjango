import requests


def calcular_frete(cep_destino, peso_total, valor_total):
    url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'
    params = {
        'nCdEmpresa': '',
        'sDsSenha': '',
        'nCdServico': '40010',
        'sCepOrigem': '01310200',
        'sCepDestino': cep_destino,
        'nVlPeso': peso_total,
        'nCdFormato': 1,
        'nVlComprimento': 20,
        'nVlAltura': 20,
        'nVlLargura': 20,
        'nVlValorDeclarado': valor_total,
        'sCdMaoPropria': 'N',
        'nVlDiametro': 0,
        'sCdAvisoRecebimento': 'N',
        'StrRetorno': 'xml',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    xml = response.content.decode('ISO-8859-1')
    valor_frete = float(xml.split('<Valor>')[1].split(
        '</Valor>')[0].replace(',', '.'))
    prazo_entrega = int(xml.split('<PrazoEntrega>')[
                        1].split('</PrazoEntrega>')[0])

    return valor_frete, prazo_entrega
