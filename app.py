import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicles US", page_icon=":car:", layout="wide") #configurando a página
st.title("Vehicles analysis in the USA") #adicionado título

car_data = pd.read_csv(r"vehicles_clean.csv") # lendo os dados

st.sidebar.header("Filters") #adicionado título na barra lateral
min_p, max_p = int(car_data['price'].min()), int(car_data['price'].max())
p1, p2 = st.sidebar.slider("Select price range", min_p, max_p, (min_p, max_p)) #adicionado slider para selecionar faixa de preço
car_data = car_data[(car_data['price'] >= p1) & (car_data['price'] <= p2)] # filtrando os dados com base na faixa de preço selecionada
 
#titulo adicionado
st.header("Data viewer")
include_small = st.checkbox("Include cars with price below 1000", value=False)


if include_small:
    car_data = car_data[car_data['price'] < 1000]
    
else:
    counts = car_data['model'].value_counts()
    big_mans = counts[counts > 100].index
    car_data = car_data[car_data['model'].isin(big_mans)]
    
st.dataframe(car_data) # exibindo os dados filtrados



#caixa de seleção adicionado
build_histogram = st.checkbox("Build histogram", value=True)
build_scatter = st.checkbox("Build scatter plot", value=True)

if build_histogram:
    st.write("Histogram of odometer")
    fig = px.histogram(car_data, x='odometer', color='type', nbins=30, title="Histogram of odometer by type")
    st.plotly_chart(fig, use_container_width=True)
    
if build_scatter:
    st.write("Scatter plot of price vs odometer")
    fig2 = px.scatter(car_data, x='odometer', y='price', color='type', title="Scatter plot of price vs odometer by type")
    st.plotly_chart(fig2, use_container_width=True)

  
st.header("Compare price distribution by model")
man_list = sorted(car_data['model'].dropna().unique())
if len(man_list) >= 2:
    col1, col2 = st.columns(2)
    with col1:
        defalt1 = man_list.index('ford') if 'ford' in man_list else 0
        man1 = st.selectbox("Select model 1", man_list, index=defalt1)
    with col2:
        defalt2 = man_list.index('chevrolet') if 'chevrolet' in man_list else 0
        man2 = st.selectbox("Select model 2", man_list, index=defalt2)
        
    normalize = st.checkbox("Normalize histogram", value=False)
    compare_df = car_data[car_data['model'].isin([man1, man2])]

    fig3 = px.histogram(compare_df, x='price', color='model', barmode='overlay', histnorm='percent' if normalize else None)
    
    fig3.update_layout(yaxis_title='Percentage' if normalize else 'Count')
    st.plotly_chart(fig3, use_container_width=True)
