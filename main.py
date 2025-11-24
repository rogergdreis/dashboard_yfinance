import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


# criar as funções de carregamento de dados
    # Cotações

@st.cache_data
def carregar_dados(empresas):
    df = yf.download(empresas, start="2010-01-01", end="2025-11-01", interval="1d", group_by="ticker")
    close = pd.concat({t: df[t]["Close"] for t in empresas}, axis=1)
    close = close.dropna(how="all")
    return close

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv('IBOV.csv', sep=';')
    tickers = list(base_tickers['Código'])
    tickers = [item + '.SA' for item in tickers]
    return tickers

acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

# dashboard com streamlit

st.write("""
# Ações
""")

# prepara as visualizações = filtros
st.sidebar.header('Filtros')

# filtro de ações
lista_acoes = st.sidebar.multiselect('Escolha as ações para visualizar', dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: 'Close'})

# filtro de datas
if not isinstance(data_inicial, datetime):
    data_inicial = pd.to_datetime(data_inicial).to_pydatetime()
if not isinstance(data_final, datetime):
    data_final = pd.to_datetime(data_final).to_pydatetime()
intervalo_data = st.sidebar.slider('Selecione o período', min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final),step=timedelta(days=1))
dados = dados.loc[intervalo_data[0]:intervalo_data[1]]   

# criar grafico
st.line_chart(dados)

texto_performance_ativos = ''

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={'Close': acao_unica})

for acao in lista_acoes:
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)
    if performance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f'  \n{acao}: :green[{performance_ativo:.1%}]'
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f'  \n{acao}: :red[{performance_ativo:.1%}]'
    else:
        texto_performance_ativos = texto_performance_ativos + f'  \n{acao}: {performance_ativo:.1%}'

st.write(f"""
### Performance dos Ativos
Essa foi a performance de cada ativo no periodo selecionado:

{texto_performance_ativos}
         """)