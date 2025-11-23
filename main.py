import streamlit as st
import pandas as pd
import yfinance as yf

# criar as funções de carregamento de dados
    # Cotações

@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2025-11-01")
    cotacoes_acao = cotacoes_acao[["Close"]]
    return cotacoes_acao

# prepara as visualizações
dados = carregar_dados('ITUB4.SA')

# dashboard com streamlit

st.write("""
# Ações
""")

# criar grafico
st.line_chart(dados)