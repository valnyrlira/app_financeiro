from itertools import count
from matplotlib import ticker
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import investpy as inv
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import fundamentus as fd

def home():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title('Home')
        st.markdown('---')

def panorama():
    st.title('Panorama do mercado')
    st.markdown(date.today().strftime('%d/%m/%Y'))

    st.subheader('Mercados pelo mundo')

    dict_tickers = {
        'Bovespa': '^BVSP',
        'S&P500': '^GSPC',
        'NASDAQ': '^IXIC',
        'DAX': '^GDAXI',
        'FTSE 100': '^FTSE',
        'CRUID OIL': 'CL=F',
        'GOLD': 'GC=F',
        'BITCOIN': 'BTC-USD',
        'ETHEREUM': 'ETH-USD'
    }

    df_info = pd.DataFrame({'Ativo': dict_tickers.keys(), 'Ticker': dict_tickers.values()})
    #st.write(df_info)
    df_info['Ult. Valor'] = ''
    df_info['%'] = ''
    count = 0

    with st.spinner('Baixando cotações...'):
        for ticker in dict_tickers.values():
            cotacoes = yf.download(ticker, period='5d')['Adj Close']
            variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
            df_info['Ult. Valor'][count] = round(cotacoes.iloc[-1], 2)
            df_info['%'][count] = round(variacao, 2)
            count += 1
    #st.write(df_info)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(df_info['Ativo'][0], value=df_info['Ult. Valor'][0], delta=str(df_info['%'][0]) + '%')
        st.metric(df_info['Ativo'][1], value=df_info['Ult. Valor'][1], delta=str(df_info['%'][1]) + '%')
        st.metric(df_info['Ativo'][2], value=df_info['Ult. Valor'][2], delta=str(df_info['%'][2]) + '%')

    with col2:
        st.metric(df_info['Ativo'][3], value=df_info['Ult. Valor'][3], delta=str(df_info['%'][3]) + '%')
        st.metric(df_info['Ativo'][4], value=df_info['Ult. Valor'][4], delta=str(df_info['%'][4]) + '%')
        st.metric(df_info['Ativo'][5], value=df_info['Ult. Valor'][5], delta=str(df_info['%'][5]) + '%')

    with col3:
        st.metric(df_info['Ativo'][6], value=df_info['Ult. Valor'][6], delta=str(df_info['%'][6]) + '%')
        st.metric(df_info['Ativo'][7], value=df_info['Ult. Valor'][7], delta=str(df_info['%'][7]) + '%')
        st.metric(df_info['Ativo'][8], value=df_info['Ult. Valor'][8], delta=str(df_info['%'][8]) + '%')

    st.markdown('---')
    st.subheader('Comportamento durante o dia')

    lista_indices = ['IBOV', 'S&P500', 'NASDAQ']
    indice = st.selectbox('Selecione o Índice:', lista_indices)

    if indice == 'IBOV':
        indice_diario = yf.download('^BVSP', period='1d', interval='5m')
    if indice == 'S&P500':
        indice_diario = yf.download('^GSPC', period='1d', interval='5m')
    if indice == 'NASDAQ':
        indice_diario = yf.download('^IXIC', period='1d', interval='5m')

    fig = go.Figure(data=[go.Candlestick(x=indice_diario.index,
                                        open=indice_diario['Open'],
                                        high=indice_diario['High'],
                                        low=indice_diario['Low'],
                                        close=indice_diario['Close'])])
    fig.update_layout(title=indice, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

    lista_acoes = ['PETR4.SA', 'VALE3.SA', 'EQTL3.SA', 'CSNA3.SA']
    acao = st.selectbox('Selecione a ação:', lista_acoes)

    hist_acao = yf.download(acao, period='1d', interval='5m')  

    fig = go.Figure(data=[go.Candlestick(x=hist_acao.index,
                                        open=hist_acao['Open'],
                                        high=hist_acao['High'],
                                        low=hist_acao['Low'],
                                        close=hist_acao['Close'])])
    fig.update_layout(title=acao, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

def mapa_mensal():
    st.title('Análise de Retornos Mensais')

    with st.expander('Escolha', expanded=True):
        opcao = st.radio('Selecione:', ['Indices', 'Ações'])

    if opcao == 'Indices':
        with st.form(key='form_indice'):
            ticker = st.selectbox('Indice', ['Bovespa', 'Financials', 'Basic Materials'])
            analisar = st.form_submit_button('Analisar')
    else:
        with st.form(key='form_acoes'):
            ticker = st.selectbox('Ações', ['PETR4', 'VALE3', 'EQTL3'])         
            analisar = st.form_submit_button('Analisar')
    
    if analisar:
        data_inicial = '01/12/1999'
        data_final = '31/12/2022'

        if opcao == 'Indices':
            retornos = inv.get_index_historical_data(ticker, country='brazil', from_date=data_inicial,
                                                    to_date=data_final, interval='Monthly')['Close'].pct_change()
        else:
            retornos = inv.get_stock_historical_data(ticker, country='brazil', from_date=data_inicial,
                                                    to_date=data_final, interval='Monthly')['Close'].pct_change()
       
        # st.write(retornos)

        # Separar e agrupar os anos e meses
        retorno_mensal = retornos.groupby([retornos.index.year.rename('Year'), retornos.index.month.rename('Month')]).mean()
        # st.write(retorno_mensal)

        tabela_retornos = pd.DataFrame(retorno_mensal)
        tabela_retornos = pd.pivot_table(tabela_retornos, values='Close', index='Year', columns='Month')
        tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        # st.write(tabela_retornos)

        fig, ax = plt.subplots(figsize=(12, 9))
        cmap = sns.color_palette('RdYlGn', 50)
        sns.heatmap(tabela_retornos, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.02,
                    vmin=-0.02, cbar=False, linewidths=1, xticklabels=True, yticklabels=True, ax=ax)
        ax.set_title(ticker, fontsize=18)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='12')
        ax.set_xticklabels(ax.get_xticklabels(), fontsize='12')
        ax.xaxis.tick_top()
        plt.ylabel('')
        st.pyplot(fig)

        stats = pd.DataFrame(tabela_retornos.mean(), columns=['Media'])
        stats['Mediana'] = tabela_retornos.median()
        stats['Maior'] = tabela_retornos.max()
        stats['Menor'] = tabela_retornos.min()
        stats['Positivos'] = tabela_retornos.gt(0).sum()/tabela_retornos.count()
        stats['Negativos'] = tabela_retornos.le(0).sum()/tabela_retornos.count()
        st.write(stats)

        stats_a = stats[['Media', 'Mediana', 'Maior', 'Menor']]
        stats_a = stats_a.transpose()

        fig, ax = plt.subplots(figsize=(12, 2.5))
        sns.heatmap(stats_a, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.02,
                    vmin=-0.02, cbar=False, linewidths=1, xticklabels=True, yticklabels=True, ax=ax)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='11')
        st.pyplot(fig)

        stats_b = stats[['Positivos', 'Negativos']]
        stats_b = stats_b.transpose()

        fig, ax = plt.subplots(figsize=(12, 1.5))
        sns.heatmap(stats_b, annot=True, fmt='.2%', center=0, vmax=0.02,
                    vmin=-0.02, cbar=False, linewidths=1, xticklabels=True, yticklabels=True, ax=ax)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='11')
        st.pyplot(fig)


def fundamentos():
    st.title('Informações sobre Fundamentos')

    lista_tickers = fd.list_papel_all()
    #st.write(lista_tickers)

    comparar = st.checkbox('Comparar 2 ativos')

    col1, col2 = st.columns(2)
    with col1:
        with st.expander('Ativo 1:', expanded=True):
            papel1 = st.selectbox('Selecione o ativo 1', lista_tickers)
            info_papel1 = fd.get_detalhes_papel(papel1)
            st.write('**Empresa:**', info_papel1['Empresa'][0])
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Valor de Mercado:**', info_papel1['Valor_de_mercado'][0])
            st.write('**Dívida Bruta:**', info_papel1['Div_Bruta'][0])
            st.write('**Dívida Líquida:**', info_papel1['Div_Liquida'][0])
            st.write('**P/L:**', info_papel1['PL'][0])
            st.write('**DY:**', info_papel1['Div_Yield'][0])

    if comparar:
        with col2:
            with st.expander('Ativo 2:', expanded=True):
                papel2 = st.selectbox('Selecione o ativo 2', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Valor de Mercado:**', info_papel2['Valor_de_mercado'][0])
                st.write('**Dívida Bruta:**', info_papel2['Div_Bruta'][0])
                st.write('**Dívida Líquida:**', info_papel2['Div_Liquida'][0])
                st.write('**P/L:**', info_papel2['PL'][0])
                st.write('**DY:**', info_papel2['Div_Yield'][0])

        





def main():
    st.sidebar.image('logo1.png', width=200)
    st.sidebar.title('App Financeiro')
    st.sidebar.markdown('---')
    lista_menu = ['Home', 'Panorama do Mercado', 'Rentabilidade Mensal', 'Fundamentos']
    escolha = st.sidebar.radio('Escolha a opção:', lista_menu)

    if escolha == 'Home':
        home()
    if escolha == 'Panorama do Mercado':
        panorama()
    if escolha == 'Rentabilidade Mensal':
        mapa_mensal()
    if escolha == 'Fundamentos':
        fundamentos()


main()

