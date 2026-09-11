import streamlit as st         # importando a biblioteca streamlit
import pandas as pd            # importando a biblioteca pandas
import plotly.express as px    # importando a biblioteca plotly express

st.set_page_config(page_title="Vehicles US", page_icon=":car:", layout="wide") #configurando a página


car_data = pd.read_csv("vehicles_clean.csv") #carregando os dados

st.title("Vehicles Analysis in the USA") #adicionado título

st.sidebar.header("Filters") #adicionado título na barra lateral
min_p, max_p = int(car_data['price'].min()), int(car_data['price'].max()) #adicionado variáveis para armazenar o preço mínimo e máximo dos carros
p1, p2 = st.sidebar.slider("Select price range", min_p, max_p, (min_p, max_p)) #adicionado slider para selecionar faixa de preço

st.header("Data Viewer") #adicionado título para a seção de visualização de dados
include_small = st.checkbox("Include cars with price below 1000", value=False)

if include_small: #adicionado checkbox para incluir carros com preço abaixo de 1000
    car_data = car_data[car_data['price'] < 1000]
else: # filtrando os dados para incluir apenas carros com preço acima de 1000
    car_data = car_data[(car_data['price'] >= p1) & (car_data['price'] <= p2)]
    counts = car_data['model'].value_counts()
    big_mans = counts[counts > 100].index
    car_data = car_data[car_data['model'].isin(big_mans)]

st.dataframe(car_data) # exibindo os dados filtrados

#caixa de seleção adicionado
build_histogram = st.checkbox("Build histogram", value=True)
build_scatter = st.checkbox("Build scatter plot", value=True)

if build_histogram: #adicionado checkbox para construir histograma
    st.subheader("Histogram of Odometer")
    fig = px.histogram(car_data, x='odometer', color='type', nbins=30, title="Histogram of Odometer by Type")
    st.plotly_chart(fig, use_container_width=True)
    
if build_scatter: #adicionado checkbox para construir scatter plot
    st.subheader("Scatter Plot of Price vs Odometer")
    fig2 = px.scatter(car_data, x='odometer', y='price', color='type', title="Scatter Plot of Price vs Odometer by Type", hover_data=['model'])
    st.plotly_chart(fig2, use_container_width=True)

# caixa de seleção para comparar distribuições de preço por modelo
st.header("Compare Price Distribution by Model")
man_list = sorted(car_data['model'].dropna().unique())

if len(man_list) >= 2: #adicionado verificação para garantir que haja pelo menos dois modelos para comparar
    col1, col2 = st.columns(2)
    with col1: #adicionado coluna para selecionar o primeiro modelo
        default1 = man_list.index('ford') if 'ford' in man_list else 0
        man1 = st.selectbox("Select Model 1", man_list, index=default1)
    with col2: #adicionado coluna para selecionar o segundo modelo
        default2 = man_list.index('chevrolet') if 'chevrolet' in man_list else min(1, len(man_list)-1)
        man2 = st.selectbox("Select Model 2", man_list, index=default2)
        
    normalize = st.checkbox("Normalize histogram", value=False) #adicionado checkbox para normalizar o histograma
    compare_df = car_data[car_data['model'].isin([man1, man2])]

    fig3 = px.histogram(compare_df, x='price', color='model', barmode='overlay', 
                        histnorm='percent' if normalize else None,
                        title=f"Price Comparison: {man1} vs {man2}") # adicionado histograma para comparar distribuições de preço por modelo
    
    fig3.update_layout(yaxis_title='Percentage' if normalize else 'Count') # atualizando o título do eixo y com base na normalização
    st.plotly_chart(fig3, use_container_width=True)
else: #adicionado aviso caso não haja modelos suficientes para comparar
    st.warning("Not enough models in the selected price range to compare.")
