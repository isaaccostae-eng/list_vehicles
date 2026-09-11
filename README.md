# 🚗 Vehicles Analysis in the USA

### Dashboard interativo para análise de anúncios de veículos nos EUA.         [App.Render](https://list-vehicles.onrender.com/)                       

### Funcionalidades                           
-**Data Viewer com tabela**          
-**Filtros com faixa de preço e opção de incluir veículos abaixo de $1000**           
-**Checkbox interativo**                                           
-**Histograma:** distribuição de quilometragem por tipo de veículo              
-**Gráfico de dispersão:** relação preço vs quilometragem por tipo                           
-**Comparativo:** distribuição de preço por modelo (model 1 vs model 2) com opção de normalizar                        

### Tratamento de dados                       
-**Criado 'vehicles_clean.csv:**         
-**Remoção de duplicados**                                    
-**Preenchimento de nulos:** 'model_year', 'cylinders', 'odometer' com mediana e 'paint_color' com 'unknowm'                                  
-**Remoção** apenas de linhas sem 'price' ou 'model'                                            

### Utilizados                                  
- Python
- Streamlit
- Pandas
- Plotly Express
- Render (deploy)
