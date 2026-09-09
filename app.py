import streamlit as st 
import pandas as pd
import plotly_express as px

car_data = pd.read_csv("vehicles.csv")

#titulo adicionado
[st.header("Vehicle Data Analysis")]

#botao adicionado
hist_button = st.button("show histogram")

if hist_button:
    st.write('Criando um histograma para o conjunto de dados de anúncios de vendas de carros')
    fig = px.histogram(car_data, x= 'odometer')
    st.plotly_chart(fig, use_container_width=True) 

disp_button = st.button("show dispersion")

if disp_button:
    st.write('Criando um gráfico de dispersão para o conjunto de dados de anúncios de vendas de carros')
    fig = px.scatter(car_data, x= 'odometer')
    st.plotly_chart(fig, use_container_width=True)
    
build_histogram = st.checkbox('Criar um histograma')

if build_histogram: # se a caixa de seleção for selecionada
  st.write('Criando um histograma para a coluna odometer')
  fig = px.histogram(car_data, x= 'odometer')
  st.plotly_chart(fig, use_container_width=True)
  
  