# 🍍 Tenda das Frutas | Analytics Dashboard

> Um sistema completo de automação de vendas, registo de caixa e análise de dados interativa desenvolvido em Python e Streamlit para fins de portfólio profissional.

  

## 🎯 Sobre o Projeto

A **Tenda das Frutas** simula o ecossistema operacional de um comércio real, cobrindo desde a captação e validação de transações no terminal até à visualização executiva de indicadores de desempenho (KPIs) em tempo real. O projeto foi estruturado com foco em **Data Storytelling**, engenharia de dados leve e boas práticas de visualização analítica.

## 🛠️ Tecnologias e Stack Utilizada

-   **Linguagem:** Python 3.10+
-   **Manipulação e Engenharia de Dados:** Pandas, Glob, Datetime
-   **Interface e Dashboard Web:** Streamlit
-   **Visualização de Dados:** Plotly (Gráficos de linha temporais, barras horizontais e rankings)
-   **Controlo de Versão:** Git & GitHub

## 📊 Principais Funcionalidades

1.  **Registo Automatizado de Vendas (****tenda\_frutas.py****):**
    -   Registo de clientes, cálculo automático de descontos por volume e gestão de formas de pagamento (**PIX, Dinheiro com cálculo de troco, Cartão de Débito e Crédito parcelado em até 3x**).
    -   Persistência modular diária estruturada em ficheiros CSV (vendas\_DD\_MM\_AAAA.csv).
2.  **Consolidação Mensal (****analise\_mensal.py****):**
    -   Agregação dinâmica de múltiplos ficheiros diários utilizando padrões de busca globais.
    -   Relatórios automáticos de faturamento total, ticket médio, distribuição de meios de pagamento e ranking de clientes.
3.  **Dashboard Executivo Web (****app.py****):**
    -   **Filtros Hierárquicos em Cascata:** Navegação flexível por Ano, Mês e Dia.
    -   **Cartões de KPI:** Indicadores instantâneos de Faturamento, Total de Vendas, Ticket Médio e Clientes Atendidos.
    -   **Gráficos de Alta Precisão (Tema Dark):** Evolução temporal de vendas por hora e ranking de clientes por volume de compras utilizando gráficos de barras horizontais (seguindo preceitos rigorosos de _data storytelling_ para evitar distorções visuais).

## 🚀 Como Executar o Projeto Localmente

1.  **Clonar o repositório:** git clone https://github.com/mv-teixeira/tenda\_frutas.git cd tenda\_frutas
2.  **Instalar as dependências:** pip install -r requirements.txt
3.  **Executar o script de registo de vendas (opcional para gerar dados locais):** python tenda\_frutas.py
4.  **Executar o Dashboard Interativo:** streamlit run app.py

## 📁 Estrutura do Repositório

-   vendas\_DD\_MM\_AAAA.csv - Bases de dados diárias geradas dinamicamente
-   tenda\_frutas.py - Script CLI para registo transacional e regras de negócio
-   consolidador\_vendas.py - Script de consolidação e relatórios globais do mês
-   app.py - Aplicação web em Streamlit (Dashboard Analítico)
-   README.md - Documentação técnica do projeto

## 👨‍💻 Autor

Desenvolvido por **Marcus Vinícius da Silva Reis Teixeira** como parte do portfólio focado em transição de carreira para **Análise e Engenharia de Dados**.