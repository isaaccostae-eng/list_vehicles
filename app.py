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
    
st.header("Compare price distribuition by manufacturer")
man_list = sorted(car_data['manufacturer'].dropna().unique())
if len(man_list) >= 2:
    col1, col2 = st.columns(2)
    with col1:
        defalt1 = man_list.index('ford') if 'ford' in man_list else 0
        man1 = st.selectbox("Select manufacturer 1", man_list, index=defalt1)
    with col2:
        defalt2 = man_list.index('chevrolet') if 'chevrolet' in man_list else 0
        man2 = st.selectbox("Select manufacturer 2", man_list, index=defalt2)
        
    normalize = st.checkbox("Normalize histogram", value=False)
    compare_df = car_data[car_data['manufacturer'].isin([man1, man2])]

    fig3 = px.histograma(compare_df, x='price', color='manufacturer', barmode='overlay', histnorm='percent' if normalize else None, title=f'Price distribution: {man1} vs {man2}')
    
    fig3.update_Layout(yaxis_title='Percentage' if normalize else 'Count')
    st.plotly_chart(fig3, use_container_width=True)
        