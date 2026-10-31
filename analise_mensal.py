import glob
import datetime
import pandas as pd

# Define o mês e ano atual no formato do arquivo (ex: 10_2026 para Outubro de 2026)
# Ou pode definir manualmente, ex: mes_ano_atual = "10_2026"
mes_ano_atual = datetime.datetime.now().strftime("%m_%Y")

# Cria o padrão de busca dinâmico para o mês corrente
padrao_busca = f"vendas_*_{mes_ano_atual}.csv"
arquivos_mes = glob.glob(padrao_busca)

print(
  f"📁 Buscando arquivos para o período atual ({mes_ano_atual}):"
  f" {arquivos_mes}"
)

if not arquivos_mes:
  print("❌ Nenhum arquivo encontrado para este mês.")
else:
  # Lendo e consolidando todos os arquivos do mês em um único DataFrame
  lista_dfs = [pd.read_csv(arq) for arq in arquivos_mes]
  df_mensal = pd.concat(lista_dfs, ignore_index=True)

  print("\n--- 📋 DADOS CONSOLIDADOS DO MÊS (PRIMEIRAS LINHAS) ---")
  print(df_mensal.head())

  # Relatório de Indicadores Globais (KPIs)
  print("\n" + "=" * 40)
  print("📊 RELATÓRIO ANALÍTICO CONSOLIDADO (MÊS)")
  print("=" * 40)

  total_vendas = df_mensal.shape[0]
  faturamento_total = df_mensal["Valor Total"].sum()
  ticket_medio = df_mensal["Valor Total"].mean()

  print(f"• Total de Atendimentos no Mês: {total_vendas}")
  print(f"• Faturamento Total do Mês: R$ {faturamento_total:.2f}")
  print(f"• Ticket Médio Geral: R$ {ticket_medio:.2f}")

  # Distribuição simplificada por forma de pagamento principal
  print("\n--- 💳 DISTRIBUIÇÃO POR FORMA DE PAGAMENTO ---")


  # Criando uma categoria principal limpa para relatórios executivos
  def simplificar_pagamento(texto):
    texto_upper = str(texto).upper()
    if "PIX" in texto_upper:
      return "PIX"
    elif "DÉBITO" in texto_upper:
      return "Cartão de Débito"
    elif "CRÉDITO" in texto_upper:
      return "Cartão de Crédito"
    elif "DINHEIRO" in texto_upper:
      return "Dinheiro"
    return "Outros"


  df_mensal["Tipo_Pagamento"] = df_mensal["Forma de Pagamento"].apply(simplificar_pagamento)
  contagem_pagamentos = df_mensal["Tipo_Pagamento"].value_counts()
  print(contagem_pagamentos)

  # Faturamento por Forma de Pagamento
  print("\n--- 💰 FATURAMENTO POR MEIO DE PAGAMENTO ---")
  faturamento_por_pag = df_mensal.groupby("Tipo_Pagamento")["Valor Total"].sum().reset_index()
  faturamento_por_pag = faturamento_por_pag.sort_values(by="Valor Total", ascending=False)
  print(faturamento_por_pag.to_string(index=False))

  # Ranking de Clientes (Quem mais comprou no mês)
  print("\n--- 🏆 TOP CLIENTES (MAIOR VOLUME DE COMPRAS) ---")
  top_clientes = (
    df_mensal.groupby("Cliente")["Valor Total"].sum().reset_index()
  )
  top_clientes = top_clientes.sort_values(by="Valor Total", ascending=False)
  print(top_clientes.to_string(index=False))
  print("=" * 40)

