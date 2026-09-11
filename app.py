import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicles US", page_icon=":car:", layout="wide") #configurando a página

@st.cache_data # deixa o app 10x mais rápido, não lê o csv toda hora
def load_data():
    return pd.read_csv("vehicles_clean.csv")

car_data_original = load_data()

st.title("Vehicles Analysis in the USA") #adicionado título
st.sidebar.header("Filters") #adicionado título na barra lateral

# --- SIDEBAR FILTERS ---
min_p, max_p = int(car_data_original['price'].min()), int(car_data_original['price'].max())
p1, p2 = st.sidebar.slider("Select price range", min_p, max_p, (min_p, max_p)) #adicionado slider para selecionar faixa de preço

# filtra sem perder o original
filtered_data = car_data_original[
    (car_data_original['price'] >= p1) & (car_data_original['price'] <= p2)
].copy()
 
# --- DATA VIEWER ---
st.header("Data Viewer")
include_small = st.checkbox("Include cars with price below 1000", value=False)

# CORREÇÃO DA LÓGICA AQUI
if not include_small:
    filtered_data = filtered_data[filtered_data['price'] >= 1000]
else:
    # só mostra modelos populares pra não travar a tabela
    counts = filtered_data['model'].value_counts()
    popular_models = counts[counts > 100].index
    if len(popular_models) > 0:
        filtered_data = filtered_data[filtered_data['model'].isin(popular_models)]
    
st.dataframe(filtered_data) # exibindo os dados filtrados

# --- CHARTS ---
#caixa de seleção adicionado
build_histogram = st.checkbox("Build histogram", value=True)
build_scatter = st.checkbox("Build scatter plot", value=True)

if build_histogram:
    st.subheader("Histogram of Odometer")
    fig = px.histogram(filtered_data, x='odometer', color='type', nbins=30, title="Histogram of Odometer by Type")
    st.plotly_chart(fig, use_container_width=True)
    
if build_scatter:
    st.subheader("Scatter Plot of Price vs Odometer")
    fig2 = px.scatter(filtered_data, x='odometer', y='price', color='type', title="Scatter Plot of Price vs Odometer by Type", hover_data=['model'])
    st.plotly_chart(fig2, use_container_width=True)

# --- COMPARE ---
st.header("Compare Price Distribution by Model")
man_list = sorted(filtered_data['model'].dropna().unique())

if len(man_list) >= 2:
    col1, col2 = st.columns(2)
    with col1:
        default1 = man_list.index('ford') if 'ford' in man_list else 0
        man1 = st.selectbox("Select Model 1", man_list, index=default1)
    with col2:
        default2 = man_list.index('chevrolet') if 'chevrolet' in man_list else min(1, len(man_list)-1)
        man2 = st.selectbox("Select Model 2", man_list, index=default2)
        
    normalize = st.checkbox("Normalize histogram", value=False)
    compare_df = filtered_data[filtered_data['model'].isin([man1, man2])]

    fig3 = px.histogram(compare_df, x='price', color='model', barmode='overlay', 
                        histnorm='percent' if normalize else None,
                        title=f"Price Comparison: {man1} vs {man2}")
    
    fig3.update_layout(yaxis_title='Percentage' if normalize else 'Count')
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Not enough models in the selected price range to compare.")