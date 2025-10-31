import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONTROL DE ACCESO BÁSICO ---
st.title("Dashboard de Ciencia de Datos")

# Login básico
password = st.text_input("Ingrese la contraseña", type="password")
if password != "mi_clave_segura":
    st.warning("Acceso restringido. Ingrese la contraseña correcta.")
    st.stop()

# --- CARGA DE DATOS ---
df = pd.read_csv("dataset_final.csv")
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# --- VISUALIZACIONES ---
st.subheader("Visualización interactiva")

columna = st.selectbox("Selecciona una columna numérica para analizar", df.select_dtypes("number").columns)

fig = px.histogram(df, x=columna, nbins=20, title=f"Distribución de {columna}")
st.plotly_chart(fig)
