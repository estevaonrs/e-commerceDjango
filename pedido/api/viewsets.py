import requests

# Configurações do Asaas
BASE_URL = "https://www.asaas.com/api/v3"
CLIENT_ID = "SEU_CLIENT_ID"
CLIENT_SECRET = "SEU_CLIENT_SECRET"
ACCESS_TOKEN = None  # Será definido mais tarde

# Função para obter o token de acesso


def obter_token_acesso():
    global ACCESS_TOKEN

    auth_endpoint = f"{BASE_URL}/auth"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(auth_endpoint, data=data)
    if response.status_code == 200:
        ACCESS_TOKEN = response.json().get("access_token")
    else:
        print("Erro ao obter o token de acesso.")
        print(response.json())

# Função para criar um cliente no Asaas


def criar_cliente(nome, email, cpf_cnpj):
    clientes_endpoint = f"{BASE_URL}/customers"
    headers = {
        "Content-Type": "application/json",
        "access_token": ACCESS_TOKEN
    }
    data = {
        "name": nome,
        "email": email,
        "cpfCnpj": cpf_cnpj
        # Outros campos relevantes para o cliente
    }

    response = requests.post(clientes_endpoint, headers=headers, json=data)
    if response.status_code == 201:
        cliente_id = response.json().get("id")
        print(f"Cliente criado com sucesso. ID: {cliente_id}")
        return cliente_id
    else:
        print("Erro ao criar o cliente.")
        print(response.json())

# Função para criar uma cobrança no Asaas


def criar_cobranca(cliente_id, valor, descricao):
    cobrancas_endpoint = f"{BASE_URL}/payments"
    headers = {
        "Content-Type": "application/json",
        "access_token": ACCESS_TOKEN
    }
    data = {
        "customer": cliente_id,
        "billingType": "BOLETO",  # Ou "CREDIT_CARD" para cartão de crédito
        "value": valor,
        "description": descricao
        # Outros campos relevantes para a cobrança
    }

    response = requests.post(cobrancas_endpoint, headers=headers, json=data)
    if response.status_code == 201:
        cobranca_id = response.json().get("id")
        print(f"Cobrança criada com sucesso. ID: {cobranca_id}")
        return cobranca_id
    else:
        print("Erro ao criar a cobrança.")
        print(response.json())

# Função para redirecionar o usuário para o link de pagamento do Asaas


def redirecionar_para_pagamento(cobranca_id):
    cobranca_endpoint = f"{BASE_URL}/payments/{cobranca_id}"
    headers = {
        "Content-Type": "application/json",
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(cobranca_endpoint, headers=headers)
    if response.status_code == 200:
        link_pagamento = response.json().get("bankSlipUrl")
        print("Redirecionando usuário para o link de pagamento:")
        print(link_pagamento)
        # Redirecione o usuário para o link de pagamento
    else:
        print("Erro ao obter o link de pagamento.")
        print(response.json())

# Fluxo principal


def main():
    obter_token_acesso()

    # Informações do cliente
    nome = "Nome do Cliente"
    email = "email@example.com"
    cpf_cnpj = "12345678900"  # CPF ou CNPJ válido

    # Informações da cobrança
    valor = 100.00
    descricao = "Descrição da cobrança"

    cliente_id = criar_cliente(nome, email, cpf_cnpj)
    cobranca_id = criar_cobranca(cliente_id, valor, descricao)
    redirecionar_para_pagamento(cobranca_id)


# Executar o fluxo principal
if __name__ == "__main__":
    main()
