# 🍎 Tenda das Frutas — Pipeline de Engenharia de Dados & Dashboard

Projeto de Engenharia de Dados para gestão transacional, tratamento de dados em lote (batch processing) e visualização executiva em tempo real.

## 🛠️ Arquitetura e Tecnologias
- **Linguagem:** Python
- **Processamento de Dados:** Pandas & Glob (Ingestão dinâmica de CSVs particionados por data)
- **Visualização Web:** Streamlit
- **Gráficos Interativos:** Plotly
- **Design System:** Custom Dark Mode (Tech/Modern com destaques em verde-mentha)

## 📁 Estrutura do Projeto
- `tenda_frutas.py`: Sistema transacional para registro diário de vendas e exportação de CSVs.
- `analise_mensal.py`: Script para consolidação e análise dos KPIs do mês.
- `app.py`: Dashboard executivo e interativo com filtros de navegação por ano e mês.
- `.streamlit/config.toml`: Configuração da identidade visual do dashboard.

## 🚀 Como Executar Localmente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt