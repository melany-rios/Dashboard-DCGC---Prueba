# ============================================
# DASHBOARD POLICIAL – STREAMLIT
# Con mapa, PDF y admin oculto
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from reportlab.pdfgen import canvas
import streamlit_authenticator as stauth
import tempfile
import io

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

st.set_page_config(
    page_title="Dashboard Institucional",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# AUTENTICACIÓN COMPATIBLE STREAMLIT CLOUD
# ==========================================================
import streamlit as st

# 👇 IMPORTACIÓN CORRECTA (universal)
import streamlit_authenticator as stauth

# --- Datos de usuarios ---
names = ["Administrador", "Invitado"]
usernames = ["admin", "invitado"]

# Contraseñas en texto plano
passwords = ["admin123", "invitado123"]

# 👇 MÉTODO UNIVERSAL PARA HASHEAR CONTRASEÑAS
hashed_passwords = stauth.Hasher(passwords).generate()

# --- Diccionario de credenciales ---
credentials = {"usernames": {}}

for i in range(len(usernames)):
    credentials["usernames"][usernames[i]] = {
        "name": names[i],
        "password": hashed_passwords[i]
    }

# --- Inicialización del autenticador ---
authenticator = stauth.Authenticate(
    credentials,
    "cookie_dashboard_dcgc",
    "cookie_key_123456789",  # puede ser cualquier string
    cookie_expiry_days=1
)

# --- Renderizar formulario de login ---
name, auth_status, username = authenticator.login("🔐 Inicio de Sesión", "main")

# --- Manejo de estados ---
if auth_status is False:
    st.error("❌ Usuario o contraseña incorrectos.")

elif auth_status is None:
    st.warning("Ingrese sus credenciales para continuar.")

elif auth_status:
    # Logout en barra lateral
    authenticator.logout("Cerrar Sesión", "sidebar")
    st.sidebar.success(f"Sesión iniciada como: **{name}**")

    # ============================================
    # CARGA DE DATOS
    # ============================================

    @st.cache_data
    def load_data():
        return (
            pd.read_csv("data/rrhh_dependencias.csv"),
            pd.read_csv("data/armamento.csv")
        )

    df_rrhh, df_armas = load_data()

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
        col3.metric("🔫 Armas registradas", df_armas.shape[0])

    # ============================================
    # 2) RECURSOS HUMANOS
    # ============================================

    if seccion == "👮‍♂️ Recursos Humanos":
        st.title("👮‍♂️ Recursos Humanos")

        col1, col2 = st.columns(2)

        # --- Jerarquías ---
        with col1:
            fig = px.bar(
                df_rrhh["jerarquia"].value_counts(),
                title="Jerarquías del Personal"
            )
            st.plotly_chart(fig, use_container_width=True)

        # --- Estado del Funcionario ---
        with col2:
            fig = px.pie(
                df_rrhh,
                names="estado_funcionario",
                title="Estado del Personal"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Personal por Dependencia")
        fig = px.bar(
            df_rrhh.groupby("dependencia").size().reset_index(name="cantidad"),
            x="dependencia", y="cantidad",
            title="Cantidad de Personal por Dependencia"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    # ============================================
    # 3) ARMAMENTO
    # ============================================

    if seccion == "🔫 Armamento":
        st.title("🔫 Estado de Armamento")

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(df_armas, names="tipo_arma", title="Tipos de Armas")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                df_armas["estado_arma"].value_counts(),
                title="Estado Operativo del Armamento"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Armas por Dependencia")
        fig = px.bar(
            df_armas.groupby("dependencia").size().reset_index(name="cantidad"),
            x="dependencia", y="cantidad",
            title="Cantidad de Armas por Dependencia"
        )
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

        mapa = folium.Map(location=[-27.8, -64.3], zoom_start=7)

        for _, row in df_rrhh.iterrows():
            dep = row["dependencia"]
            if dep in coords:
                lat, lon = coords[dep]
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{dep}",
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(mapa)

        st_folium(mapa, width=1200, height=600)

    # ============================================
    # 5) GENERAR PDF
    # ============================================

    if seccion == "📄 Reporte PDF":
        st.title("📄 Generación de Reporte PDF")

        buffer = io.BytesIO()

        c = canvas.Canvas(buffer)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, "Reporte Institucional")
        c.setFont("Helvetica", 12)

        c.drawString(50, 770, f"Total de Personal: {df_rrhh.shape[0]}")
        c.drawString(50, 750, f"Dependencias: {df_rrhh['dependencia'].nunique()}")
        c.drawString(50, 730, f"Armas Registradas: {df_armas.shape[0]}")

        c.showPage()
        c.save()

        st.download_button(
            label="📥 Descargar PDF",
            data=buffer.getvalue(),
            file_name="reporte_institucional.pdf",
            mime="application/pdf"
        )
