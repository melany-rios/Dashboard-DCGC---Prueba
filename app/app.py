# ============================================
# DASHBOARD POLICIAL – STREAMLIT
# Con mapa, PDF y admin oculto
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
from streamlit_folium import st_folium
import folium
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

st.set_page_config(
    page_title="Dashboard Institucional",
    page_icon="📊",
    layout="wide"
)

# ============================================
# LOGIN
# ============================================

names = ["Administrador", "Invitado"]
usernames = ["admin", "invitado"]
passwords = ["admin123", "invitado123"]

hashed_pw = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_pw,
    "dashboard_cookie", "secret_signature_key", cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuario o contraseña incorrectos")

if authentication_status is None:
    st.warning("Ingrese sus credenciales")

if authentication_status:

    st.sidebar.write(f"Hola, {name} 👋")
    authenticator.logout("Cerrar sesión", "sidebar")

    # ============================================
    # CARGA DE DATOS
    # ============================================

    @st.cache_data
    def load_data():
        return (
            pd.read_csv("data/rrhh_dependencias.csv"),
            pd.read_csv("data/armamento.csv")
        )

    df_rrhh, df_arm = load_data()

    # ============================================
    # MENÚ
    # ============================================

    seccion = st.sidebar.radio(
        "Navegación",
        ["📋 Inicio", "👮‍♂️ Recursos Humanos", "🔫 Armamento", "🗺 Mapa de Dependencias", "📄 Reporte PDF"]
    )

    # ============================================
    # FUNCIÓN PARA ADMIN OCULTO
    # ============================================
    def admin_page():
        st.header("🔒 Área administrativa secreta")
        st.info("Esta sección solo es visible para administradores.")
        st.write("Aquí podrías agregar:")
        st.write("- Subida de nuevos CSV")
        st.write("- Herramientas avanzadas de auditoría")
        st.write("- Configuraciones internas")
        st.write("- Panel moderador")

    if username == "admin":
        if st.sidebar.checkbox("Modo Administrador"):
            admin_page()

    # ============================================
    # 1) INICIO
    # ============================================
    if seccion == "📋 Inicio":
        st.title("📊 Dashboard Institucional – Policía")

        col1, col2, col3 = st.columns(3)
        col1.metric("👮‍♂️ Personal total", df_rrhh.shape[0])
        col2.metric("🏢 Dependencias", df_rrhh['dependencia'].nunique())
        col3.metric("🔫 Armas registradas", df_arm.shape[0])

    # ============================================
    # 2) RECURSOS HUMANOS
    # ============================================

    if seccion == "👮‍♂️ Recursos Humanos":
        st.title("👮‍♂️ Recursos Humanos")

        regiones = st.multiselect("Región", df_rrhh.region.unique())
        deps = st.multiselect("Dependencia", df_rrhh.dependencia.unique())

        df_f = df_rrhh.copy()
        if regiones:
            df_f = df_f[df_f.region.isin(regiones)]
        if deps:
            df_f = df_f[df_f.dependencia.isin(deps)]

        st.subheader("Cantidad por Jerarquía")
        fig1 = px.histogram(df_f, x="jerarquia", color="jerarquia")
        st.plotly_chart(fig1, use_container_width=True)

    # ============================================
    # 3) ARMAMENTO
    # ============================================

    if seccion == "🔫 Armamento":
        st.title("🔫 Estado de Armamento")

        fig = px.pie(df_arm, names="estado_arma", title="Estado operativo")
        st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # 4) MAPA GEOGRÁFICO
    # ============================================

    if seccion == "🗺 Mapa de Dependencias":
        st.title("🗺 Mapa Geográfico de Dependencias Policiales")

        # Diccionario con coordenadas
        coords = {
            "Departamental Nº 1 Zona Norte (Capital)": (-27.782, -64.264),
            "Departamental Nº 2 Zona Centro (Capital)": (-27.783, -64.250),
            "Departamental Nº 3 Zona Sur (Capital)": (-27.809, -64.273),
            "Departamental Nº 4 Zona Oeste (La Banda)": (-27.736, -64.259),
            "Departamental Nº 5 Zona Este (La Banda)": (-27.726, -64.220),
            "Departamental Nº 6 Las Termas": (-27.499, -64.856),
            "Departamental Nº 7 Frías": (-28.645, -65.139),
            "Departamental Nº 8 Fernández": (-27.929, -64.444),
            "Departamental Nº 9 Loreto": (-28.301, -64.195),
            "Departamental Nº 10 Nueva Esperanza": (-26.930, -64.261),
            "Departamental Nº 11 Monte Quemado": (-25.803, -62.830),
            "Departamental Nº 12 Quimilí": (-27.650, -62.416),
            "Departamental Nº 13 Añatuya": (-28.460, -62.833),
            "Departamental Nº 14 Pinto": (-28.415, -62.098),
            "Departamental Nº 15 Ojo de Agua": (-29.167, -63.233),
            "Departamental Nº 16 Los Flores (Capital)": (-27.790, -64.276)
        }

        mapa = folium.Map(location=[-27.78, -64.26], zoom_start=6)

        for _, row in df_rrhh.iterrows():
            dep = row["dependencia"]
            if dep in coords:
                lat, lon = coords[dep]
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{dep}",
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(mapa)

        st_folium(mapa, width=1200)

    # ============================================
    # 5) GENERAR PDF
    # ============================================

    if seccion == "📄 Reporte PDF":
        st.title("📄 Generación de Reporte PDF")

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(50, 750, "Reporte Institucional – Policía")
        c.drawString(50, 730, f"Total Personal: {df_rrhh.shape[0]}")
        c.drawString(50, 710, f"Dependencias: {df_rrhh['dependencia'].nunique()}")
        c.drawString(50, 690, f"Armas Registradas: {df_arm.shape[0]}")

        c.drawString(50, 660, "Generado automáticamente desde el dashboard.")
        c.showPage()
        c.save()

        st.download_button("📄 Descargar PDF", data=buffer.getvalue(), file_name="reporte.pdf")
