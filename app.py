import glob
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página do dashboard
st.set_page_config(
    page_title="Tenda das Frutas - Dashboard", page_icon="🍎", layout="wide"
)

st.title("🍎 Tenda das Frutas - Dashboard Executivo")
st.markdown(
    "Painel analítico interativo com navegação temporal e consolidação em"
    " tempo real."
)

# 1. Carregando TODOS os arquivos CSV da pasta
todos_arquivos = glob.glob("vendas_*_*_*.csv")

if not todos_arquivos:
  st.warning("⚠️ Nenhum arquivo de vendas encontrado na base de dados.")
  st.info(
      "Execute algumas vendas no seu sistema transacional para gerar os dados!"
  )
else:
  # Consolida todos os CSVs em um DataFrame global
  lista_dfs = [pd.read_csv(arq) for arq in todos_arquivos]
  df_global = pd.concat(lista_dfs, ignore_index=True)

  # Tratamento de datas para ordenação e agrupamento
  df_global["Data_DT"] = pd.to_datetime(
      df_global["Data e Hora"], format="%d/%m/%Y às %H:%M", errors="coerce"
  )
  df_global["Data_Dia"] = df_global["Data_DT"].dt.date
  df_global["Ano"] = df_global["Data_DT"].dt.year.astype(str)
  df_global["Mes_Ano"] = df_global["Data_DT"].dt.strftime("%m_%Y")

  # -------------------------------------------------------------
  # BARRA LATERAL (FILTROS DE NAVEGAÇÃO)
  # -------------------------------------------------------------
  st.sidebar.header("🔍 Filtros de Análise")

  tipo_visao = st.sidebar.radio(
      "Selecione o Nível de Análise:",
      ["Mês Específico", "Consolidado Anual (Todos os Meses)"],
  )

  if tipo_visao == "Mês Específico":
    meses_disponiveis = sorted(
        df_global["Mes_Ano"].dropna().unique(), reverse=True
    )
    mes_selecionado = st.sidebar.selectbox(
        "Escolha o Mês/Ano:", meses_disponiveis
    )
    df_filtrado = df_global[df_global["Mes_Ano"] == mes_selecionado]
    titulo_periodo = f"Período: {mes_selecionado}"
  else:
    anos_disponiveis = sorted(df_global["Ano"].dropna().unique(), reverse=True)
    ano_selecionado = st.sidebar.selectbox("Escolha o Ano:", anos_disponiveis)
    df_filtrado = df_global[df_global["Ano"] == ano_selecionado]
    titulo_periodo = f"Visão Consolidada do Ano {ano_selecionado}"

  # -------------------------------------------------------------
  # PAINEL PRINCIPAL (DASHBOARD)
  # -------------------------------------------------------------
  st.subheader(f"📊 Indicadores de Desempenho — {titulo_periodo}")

  if df_filtrado.empty:
    st.error("Nenhum dado encontrado para o filtro selecionado.")
  else:
    # 1. Cartões de Métricas (KPIs)
    total_vendas = df_filtrado.shape[0]
    faturamento_total = df_filtrado["Valor Total"].sum()
    ticket_medio = df_filtrado["Valor Total"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Atendimentos", f"{total_vendas}")
    col2.metric("Faturamento Total", f"R$ {faturamento_total:.2f}")
    col3.metric("Ticket Médio", f"R$ {ticket_medio:.2f}")

    st.markdown("---")

    # 2. Gráfico de Evolução Temporal (Faturamento Diário)
    st.subheader("📈 Evolução Diária do Faturamento")
    vendas_dia = (
        df_filtrado.groupby("Data_Dia")["Valor Total"].sum().reset_index()
    )
    vendas_dia.columns = ["Data", "Faturamento"]

    fig_linha = px.line(
        vendas_dia,
        x="Data",
        y="Faturamento",
        markers=True,
        color_discrete_sequence=["#00D1B2"],
    )
    fig_linha.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E0E6ED",
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1E2631"),
    )
    st.plotly_chart(fig_linha, width="stretch")

    st.markdown("---")

    # 3. Gráficos de Formas de Pagamento e Clientes
    col_a, col_b = st.columns(2)

    with col_a:
      st.subheader("💳 Formas de Pagamento Preferidas")
      pagamento_df = (
          df_filtrado["Forma de Pagamento"].value_counts().reset_index()
      )
      pagamento_df.columns = ["Forma de Pagamento", "Quantidade"]

      fig_pag = px.bar(
          pagamento_df,
          x="Forma de Pagamento",
          y="Quantidade",
          color="Forma de Pagamento",
          color_discrete_sequence=["#00D1B2", "#20C997", "#38D9A9", "#63E6BE"],
      )
      fig_pag.update_layout(
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font_color="#E0E6ED",
          showlegend=False,
          margin=dict(t=20, b=20, l=20, r=20),
      )
      st.plotly_chart(fig_pag, width="stretch")

    with col_b:
      st.subheader("🏆 Ranking de Clientes (Volume de Compras)")
      top_clientes = (
          df_filtrado.groupby("Cliente")["Valor Total"].sum().reset_index()
      )
      top_clientes = top_clientes.sort_values(
          by="Valor Total", ascending=False
      )
      st.dataframe(top_clientes, width="stretch", hide_index=True)

    st.markdown("---")

    # 4. Base de Dados Completa Consolidada
    st.subheader("📋 Transações do Período Selecionado")
    with st.expander("Clique para visualizar a tabela detalhada"):
      st.dataframe(
          df_filtrado.drop(
              columns=["Data_DT", "Data_Dia", "Ano", "Mes_Ano"],
              errors="ignore",
          ),
          width="stretch",
      )