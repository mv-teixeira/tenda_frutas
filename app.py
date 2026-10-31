import streamlit as st
import pandas as pd
import plotly.express as px
import glob

# 1. Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Tenda das Frutas | Analytics",
    page_icon="🍍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para visual executivo (Dark Theme)
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .kpi-card {
        background-color: #1E222D;
        border-radius: 10px;
        padding: 15px 20px;
        border-left: 5px solid #00D47E;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #A0AAB8;
        margin-bottom: 5px;
        font-weight: 500;
    }
    .kpi-value {
        font-size: 1.8rem;
        color: #FFFFFF;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)


# 2. Carregamento e consolidação dinâmica dos dados
@st.cache_data
def carregar_dados():
    arquivos = glob.glob("vendas_*.csv")
    lista_dfs = []
    for arq in arquivos:
        df_temp = pd.read_csv(arq)
        lista_dfs.append(df_temp)

    if lista_dfs:
        df_concat = pd.concat(lista_dfs, ignore_index=True)
        # Limpeza e formatação de datas
        df_concat['Data_dt'] = pd.to_datetime(df_concat['Data e Hora'], format='%d/%m/%Y às %H:%M', errors='coerce')
        df_concat['Dia'] = df_concat['Data_dt'].dt.strftime('%d/%m/%Y')
        df_concat['Mes_Ano'] = df_concat['Data_dt'].dt.strftime('%m/%Y')
        df_concat['Ano'] = df_concat['Data_dt'].dt.strftime('%Y')
        return df_concat
    return pd.DataFrame()


df = carregar_dados()

if df.empty:
    st.warning("Nenhum dado encontrado nos arquivos CSV.")
    st.stop()

# 3. Barra Lateral (Filtros Hierárquicos: Ano, Mês e Dia)
st.sidebar.image("https://img.icons8.com/color/96/strawberry.png", width=70)
st.sidebar.title("Painel de Controle")

# Filtro de Ano
anos_disponiveis = sorted(df['Ano'].dropna().unique(), reverse=True)
opcao_ano = st.sidebar.selectbox("📅 Selecione o Ano:", ["Todos os Anos"] + list(anos_disponiveis))

if opcao_ano != "Todos os Anos":
    df_filtrado_ano = df[df['Ano'] == opcao_ano]
else:
    df_filtrado_ano = df.copy()

# Filtro de Mês com base no ano selecionado
meses_disponiveis = sorted(df_filtrado_ano['Mes_Ano'].dropna().unique(), reverse=True)
opcao_mes = st.sidebar.selectbox("📆 Selecione o Mês:", ["Todos os Meses"] + list(meses_disponiveis))

if opcao_mes != "Todos os Meses":
    df_filtrado_mes = df_filtrado_ano[df_filtrado_ano['Mes_Ano'] == opcao_mes]
else:
    df_filtrado_mes = df_filtrado_ano.copy()

# Filtro de Dia com base no mês/ano selecionado
dias_disponiveis = sorted(df_filtrado_mes['Dia'].dropna().unique(), reverse=True)
opcao_dia = st.sidebar.selectbox("📌 Selecione o Dia:", ["Todos os Dias"] + list(dias_disponiveis))

# Aplicação do Filtro Final
if opcao_dia != "Todos os Dias":
    df_filtered = df_filtrado_mes[df_filtrado_mes['Dia'] == opcao_dia]
else:
    df_filtered = df_filtrado_mes.copy()

# 4. Cabeçalho Principal
st.title("🍍 Tenda das Frutas — Performance de Vendas")
st.caption("Dashboard executivo em tempo real para acompanhamento de faturamento e fluxo de caixa.")
st.markdown("---")

# 5. Métricas de Alto Impacto (KPIs)
col1, col2, col3, col4 = st.columns(4)

coluna_valor = 'Valor Total' if 'Valor Total' in df_filtered.columns else 'Valor'

total_faturado = df_filtered[coluna_valor].sum() if coluna_valor in df_filtered.columns else 0.0
total_pedidos = len(df_filtered)
ticket_medio = total_faturado / total_pedidos if total_pedidos > 0 else 0.0
clientes_unicos = df_filtered['Cliente'].nunique() if 'Cliente' in df_filtered.columns else 0

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Faturamento Total</div>
            <div class="kpi-value">R$ {total_faturado:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #00B4D8;">
            <div class="kpi-title">Total de Vendas</div>
            <div class="kpi-value">{total_pedidos}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #FF9E00;">
            <div class="kpi-title">Ticket Médio</div>
            <div class="kpi-value">R$ {ticket_medio:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #7209B7;">
            <div class="kpi-title">Clientes Atendidos</div>
            <div class="kpi-value">{clientes_unicos}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Gráficos Interativos com Plotly (Tema Dark)
graf1, graf2 = st.columns(2)

with graf1:
    st.subheader("📈 Evolução de Vendas ao Longo do Dia")
    if not df_filtered.empty and 'Data_dt' in df_filtered.columns:
        df_hora = df_filtered.set_index('Data_dt').resample('1h')[coluna_valor].sum().reset_index()
        fig_linha = px.line(
            df_hora,
            x='Data_dt',
            y=coluna_valor,
            markers=True,
            labels={'Data_dt': 'Horário', coluna_valor: 'Faturamento (R$)'},
            template="plotly_dark"
        )
        fig_linha.update_traces(line_color="#00D47E", line_width=3)
        fig_linha.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_linha, use_container_width=True)

with graf2:
    st.subheader("👥 Top Clientes por Faturamento")
    if 'Cliente' in df_filtered.columns:
        top_clientes = df_filtered.groupby('Cliente')[coluna_valor].sum().reset_index().sort_values(by=coluna_valor,
                                                                                                    ascending=True).tail(
            7)
        fig_barras = px.bar(
            top_clientes,
            x=coluna_valor,
            y='Cliente',
            orientation='h',
            labels={coluna_valor: 'Total Gasto (R$)', 'Cliente': 'Cliente'},
            template="plotly_dark",
            color=coluna_valor,
            color_continuous_scale="Viridis"
        )
        fig_barras.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)

# 7. Seção de Formas de Pagamento (Gráfico de Barras Horizontais sem "Outros")
st.markdown("---")
pag_col1, pag_col2 = st.columns(2)

with pag_col1:
    st.subheader("💳 Faturamento por Forma de Pagamento")
    if 'Forma de Pagamento' in df_filtered.columns:
        def simplificar_pagamento(texto):
            if pd.isna(texto):
                return "Dinheiro"
            texto_upper = str(texto).upper()
            if "PIX" in texto_upper:
                return "PIX"
            elif "DÉBITO" in texto_upper:
                return "Cartão de Débito"
            elif "CRÉDITO" in texto_upper:
                return "Cartão de Crédito"
            else:
                return "Dinheiro"


        df_filtered_temp = df_filtered.copy()
        df_filtered_temp['Tipo_Pagamento'] = df_filtered_temp['Forma de Pagamento'].apply(simplificar_pagamento)

        # Agrupando e ordenando para o gráfico de barras horizontais
        df_pag = df_filtered_temp.groupby('Tipo_Pagamento')[coluna_valor].sum().reset_index()
        df_pag = df_pag.sort_values(by=coluna_valor, ascending=True)

        fig_bar_pag = px.bar(
            df_pag,
            x=coluna_valor,
            y='Tipo_Pagamento',
            orientation='h',
            template="plotly_dark",
            color=coluna_valor,
            color_continuous_scale="Viridis",
            labels={coluna_valor: 'Faturamento (R$)', 'Tipo_Pagamento': 'Forma de Pagamento'}
        )
        fig_bar_pag.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis_title="Faturamento Total (R$)",
            yaxis_title=""
        )
        st.plotly_chart(fig_bar_pag, use_container_width=True)
    else:
        st.info("Coluna 'Forma de Pagamento' não encontrada nos dados.")

with pag_col2:
    st.subheader("📋 Resumo Consolidado de Pagamentos")
    if 'Forma de Pagamento' in df_filtered.columns:
        resumo_pag = df_filtered_temp.groupby('Tipo_Pagamento').agg(
            Qtd_Transacoes=(coluna_valor, 'count'),
            Faturamento_Total=(coluna_valor, 'sum')
        ).reset_index().sort_values(by='Faturamento_Total', ascending=False)
        st.dataframe(resumo_pag, use_container_width=True, hide_index=True)
    else:
        st.info("Sem dados de pagamento disponíveis.")

# 8. Tabela Detalhada com Visão Interativa
st.markdown("---")
st.subheader("📄 Registros de Vendas Detalhados")
colunas_exibir = ['Data e Hora', 'Cliente', coluna_valor,
                  'Forma de Pagamento'] if 'Forma de Pagamento' in df.columns else ['Data e Hora', 'Cliente',
                                                                                    coluna_valor]
st.dataframe(
    df_filtered[colunas_exibir],
    use_container_width=True,
    hide_index=True
)