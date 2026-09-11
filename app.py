import streamlit as st 
import pandas as pd
import plotly.express as px

car_data = pd.read_csv(r"vehicles_clean.csv") # lendo os dados
 
#titulo adicionado
st.header("Análise de dados de anúncios de vendas de carros")

#botao adicionado
hist_button = st.button("Criar histograma")

if hist_button:
    st.write('Criando um histograma para o conjunto de dados de anúncios de vendas de carros')
    fig = px.histogram(car_data, x= 'odometer')
    st.plotly_chart(fig, use_container_width=True) 

disp_button = st.button("Criar gráfico de dispersão")

if disp_button:
    st.write('Criando um gráfico de dispersão para o conjunto de dados de anúncios de vendas de carros')
    fig = px.scatter(car_data, x= 'odometer', y= 'price')
    st.plotly_chart(fig, use_container_width=True)
    
    
  