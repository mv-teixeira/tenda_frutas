# Loja de Frutas

import datetime  # Traz a ferramenta de data e hora do sistema
import csv  # Traz a ferramenta para manipular arquivos CSV
import os  # Traz ferramentas para verificar a existência de arquivos

# Definindo o nome do arquivo dinamicamente com a data atual
data_hoje_arquivo = datetime.datetime.now().strftime("%d_%m_%Y")
nome_arquivo_csv = f"vendas_{data_hoje_arquivo}.csv"

print("**     Bem Vindo(a)         **")
print("** A Tenda das Frutas **")

estoque_frutas = {
    "maçã": 3.00,
    "manga": 4.50,
    "pêra": 3.20,
    "morango": 4.00
}

# --- VARIÁVEIS DE CONTROLE DO CAIXA (Fechamento do Dia) ---
faturamento_total_dia = 0
total_clientes_atendidos = 0


# Função para exibir o catálogo de produtos
def exibir_catalogo(estoque):
    print("Confira os preços por KG:")
    for fruta, preco in estoque.items():
        print(f"- {fruta.capitalize()}: R$ {preco:.2f}")


# Função que encapsula toda a regra de negócio do desconto
def calcular_desconto(valor_total):
    if valor_total < 50:
        return valor_total, "Não há desconto aplicado."
    elif valor_total <= 100:
        return valor_total * 0.95, "Você ganhou 5% de desconto."
    else:
        return valor_total * 0.90, "Você ganhou 10% de desconto."


caixa_aberto = True

# 1. WHILE: Mantém o sistema rodando para vários clientes
while caixa_aberto:
    print("\n--- NOVO ATENDIMENTO ---")
    nome = input("Olá, como se chama? (ou digite sair para fechar o caixa): ")

    # Condição de saída
    if nome.strip().lower() == "sair":
        print("Fechando o caixa. Até logo!!")
        break

    print(f"Bem-vindo(a), {nome}!!")

    # Chamando a função do catálogo
    exibir_catalogo(estoque_frutas)

    # 2. FOR: Recolhe as quantidades usando a lista de frutas dinamicamente
    valor_total_geral = 0

    for fruta, preco in estoque_frutas.items():
        qtd = float(input(f"Quantos kg de {fruta} deseja levar? "))
        valor_total_geral += qtd * preco  # Acumula direto no total geral

    # Chamando a função de desconto
    valor_final, mensagem_desconto = calcular_desconto(valor_total_geral)

    # --- EXIBIÇÃO PRÉVIA DOS VALORES ---
    print(f"\n--- RESUMO DO PEDIDO DE {nome.upper()} ---")
    print(f"Subtotal: R$ {valor_total_geral:.2f}")
    print(f"Desconto: {mensagem_desconto}")
    print(f"VALOR TOTAL A PAGAR: R$ {valor_final:.2f}")

    # --- SISTEMA DE PAGAMENTO ---
    print("\n--- FORMAS DE PAGAMENTO ---")
    print("1 - PIX")
    print("2 - Cartão de Débito")
    print("3 - Cartão de Crédito")
    print("4 - Dinheiro")

    opcao_pagamento = input("Escolha a forma de pagamento (1, 2, 3 ou 4): ").strip()

    detalhes_pagamento = ""
    troco = 0.0

    if opcao_pagamento == "1":
        detalhes_pagamento = "PIX"

    elif opcao_pagamento == "2":
        detalhes_pagamento = "Débito à vista"

    elif opcao_pagamento == "3":
        # Se a compra for menor que 100, já define direto como à vista
        if valor_final < 100.00:
            detalhes_pagamento = "Crédito à vista"
        else:
            print("\n--- OPÇÕES DE PARCELAMENTO ---")
            print("Compras acima de R$ 100,00 podem ser parceladas em até 3x sem juros.")
            print("1 - Crédito à vista")
            print("2 - Parcelado em 2x")
            print("3 - Parcelado em 3x")

            escolha_parcelas = input("Escolha a opção de parcelamento (1, 2 ou 3): ").strip()

            if escolha_parcelas == "2":
                valor_parcela = valor_final / 2
                detalhes_pagamento = f"Crédito em 2x de R$ {valor_parcela:.2f}"
            elif escolha_parcelas == "3":
                valor_parcela = valor_final / 3
                detalhes_pagamento = f"Crédito em 3x de R$ {valor_parcela:.2f}"
            else:
                detalhes_pagamento = "Crédito à vista"

    elif opcao_pagamento == "4":
        while True:
            try:
                valor_recebido = float(input("Qual o valor em dinheiro entregue pelo cliente? R$ "))
                if valor_recebido < valor_final:
                    print(f"❌ Valor insuficiente! O total a pagar é R$ {valor_final:.2f}. Tente novamente.")
                else:
                    troco = valor_recebido - valor_final
                    detalhes_pagamento = f"Dinheiro (Recebido: R$ {valor_recebido:.2f} | Troco: R$ {troco:.2f})"
                    break
            except ValueError:
                print("❌ Por favor, digite um valor numérico válido.")
    else:
        detalhes_pagamento = "Forma não especificada"

    # --- ATUALIZANDO OS ACUMULADORES DO DIA ---
    faturamento_total_dia += valor_final
    total_clientes_atendidos += 1

    # Puxando a data e hora atual usando o módulo datetime
    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")

    # --- PERSISTÊNCIA: GRAVANDO NO ARQUIVO CSV COM CABEÇALHO ---
    # Verifica se o arquivo já existe para decidir se escrevemos o cabeçalho
    arquivo_ja_existe = os.path.exists(nome_arquivo_csv)

    with open(nome_arquivo_csv, mode="a", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)

        # Se o arquivo não existia, criamos o cabeçalho primeiro
        if not arquivo_ja_existe:
            escritor.writerow(["Data e Hora", "Cliente", "Valor Total", "Forma de Pagamento"])

        # Grava os dados da venda atual
        escritor.writerow([data_hora_atual, nome.upper(), f"{valor_final:.2f}", detalhes_pagamento])

    # Exibindo o recibo final formatado
    print(f"\n--- RESUMO DO SEU PEDIDO DE {nome.upper()} ---")
    print(f"Data: {data_hora_atual}")
    print(f"Cliente: {nome.upper()}")
    print(f"Total a pagar: R$ {valor_final:.2f}")
    print(f"Forma de Pagamento: {detalhes_pagamento}")

    if opcao_pagamento == "4":
        print(f"Troco a devolver: R$ {troco:.2f}")

    print(f"Obrigado pela preferência na Tenda das Frutas! {nome}, volte sempre 🍎\n")

# --- RELATÓRIO DE FECHAMENTO DE CAIXA ---
print("\n" + "=" * 35)
print("📊 RELATÓRIO FINAL DE FECHAMENTO DE CAIXA")
print("=" * 35)
print(f"Total de clientes atendidos: {total_clientes_atendidos}")
print(f"Faturamento total do dia: R$ {faturamento_total_dia:.2f}")
print("=" * 35)
print("Caixa encerrado com sucesso. Bom descanso!")