#Librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Funciones
def home(df):
    st.title("Cargatron")
    st.image("Taller streamlit/streamlit/puntos-recarga-madrid.jpg")
    with st.beta_expander("De que me hablas?"):
        st.write("""Ante el problema climatico al que nos enfrentamos el coche electrico se plantea como una solución posible. Aquí queremos facilitarte que encuentres tu puesto de carga más cercano.""")
    with st.echo():
        st.write("Esta forma tienen nuestros datos")
        st.dataframe(df)
    st.cache()
    st.balloons()

def datos(df):
    st.subheader("Mapa")
    map_data = df[['lat', 'lon']]
    st.map(map_data)

    st.subheader("Cargadores por distrito")
    chart_data = df[['DISTRITO','Nº CARGADORES']].groupby(['DISTRITO']).sum(['Nº CARGADORES']).sort_values(by=['DISTRITO'])
    st.bar_chart(chart_data)

    st.subheader("Cargadores por Operador")
    chart_data = df[['OPERADOR','Nº CARGADORES']].groupby(['OPERADOR']).sum(['Nº CARGADORES']).sort_values(by=['OPERADOR'])
    st.bar_chart(chart_data)

def filtrado(df):

    dis = st.sidebar.selectbox("distrito", pd.unique(df['DISTRITO'].sort_values()))
    checkdistrito = st.sidebar.checkbox('Quiero filtrar por distrito')

    cargadores = list(pd.unique(df['Nº CARGADORES']))
    car = st.sidebar.slider('Seleciona el numero de cargadores por puesto', min_value=int(min(cargadores)), max_value=int(max(cargadores)))
    checkcar = st.sidebar.checkbox('Quiero filtrar por tamaño')

    op=st.sidebar.selectbox("Operador", pd.unique(df['OPERADOR'].sort_values()))
    checkop = st.sidebar.checkbox('Quiero filtrar por operador')

    if checkdistrito:
        df = df[df['DISTRITO']== dis]

    if checkop:
        df = df[df['OPERADOR']== op]

    if checkcar:
        df = df[df["Nº CARGADORES"] >= car]

    if df.empty:
        st.warning('No hay coincidencias para los filtros')
        st.stop()

    col1, col2 = st.beta_columns(2)
    col1.subheader("Mapa")
    map_data = df[['lat', 'lon']]
    col1.map(map_data)

    col2.subheader("Cargadores por distrito:")
    chart_data = df[['DISTRITO', 'Nº CARGADORES']].groupby(['DISTRITO']).sum(['Nº CARGADORES'])
    col2.bar_chart(chart_data)

    col2.subheader("Cargadores por operador:")
    chart_data2 = df[['OPERADOR', 'Nº CARGADORES']].groupby(['OPERADOR']).sum(['Nº CARGADORES'])
    col2.bar_chart(chart_data2)

    col2.subheader("Estaciones por Nº de puestos")
    chart_data3 = df[['Nº CARGADORES']].groupby(['Nº CARGADORES']).count()
    col2.bar_chart(chart_data2)

# Main Stream lit
st.set_page_config(page_title="Cargatron", page_icon="🔌", layout='wide', initial_sidebar_state='expanded')
st.sidebar.file_uploader("Quieres introudicr otros datos?")
select = st.sidebar.selectbox("Menu:",('home', 'datos', 'filtrado'))

df = pd.read_csv("Taller streamlit/streamlit/red_recarga_acceso_publico _2021.csv",sep= ";")
df = df.rename(columns={'latidtud': 'lat', 'longitud': 'lon'})

if select == 'datos':
    datos(df)
elif select == 'home':
    home(df)
elif select == 'filtrado':
    filtrado(df)
