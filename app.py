import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicles US", page_icon=":car:", layout="wide") #configurando a página
st.title("Análise de Veículos nos EUA") #adicionado título

car_data = pd.read_csv(r"vehicles.csv") # lendo os dados

st.sidebar.header("Filtros de pesquisa") #adicionado cabeçalho na barra lateral
min_price, max_price = int(car_data['price'].min()), int(car_data['price'].max()) # definindo os valores minimos e maximos para o filtro de preço
price_filter = st.sidebar.slider("Filtrar por preço", min_value=min_price, max_value=max_price, value=(min_price, max_price))

car_data = car_data[(car_data['price'] >= price_filter[0]) & (car_data['price'] <= price_filter[1])] # aplicando o filtro de preço

#titulo adicionado
st.header("Data viewer")
include_small = st.checkbox("Incluir carros com preço abaixo de 1000", value=False)

if include_small:
    car_data = car_data[car_data['price'] < 1000]
    
else:
    counts = car_data['manufacturer'].value_counts()
    big_mans = counts[counts > 100].index
    car_data = car_data[car_data['manufacturer'].isin(big_mans)]
    
st.dataframe(car_data) # exibindo os dados filtrados



#botao adicionado
hist_button = st.button("Criar histograma")

if hist_button:
    st.write('Criando um histograma para o conjunto de dados de anúncios de vendas de carros')
    fig = px.histogram(car_data, x= 'odometer', color='type', nbins=30, title='Histograma de veículo')
    st.plotly_chart(fig, use_container_width=True) 

disp_button = st.button("Criar gráfico de dispersão")

if disp_button:
    st.write('Criando um gráfico de dispersão para o conjunto de dados de anúncios de vendas de carros')
    fig = px.scatter(car_data, x= 'odometer', y= 'price', color='type', title='Gráfico de Dispersão')
    st.plotly_chart(fig, use_container_width=True)
    
    
  