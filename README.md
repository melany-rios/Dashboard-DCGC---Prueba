# 🚔 Dashboard Institucional – Policía de Santiago del Estero  
### Ciencia de Datos · Minería de Datos · Inteligencia Artificial · Streamlit · Proyecto Final

Este proyecto consiste en el desarrollo de un **dashboard interactivo en Streamlit**, orientado al análisis y visualización de datos institucionales relativos a **Recursos Humanos**, **Dependencias Policiales** y **Armamento**.  
El objetivo principal es permitir un acceso rápido, visual y seguro a información clave para la toma de decisiones.

El proyecto forma parte de la **Tecnicatura en Ciencia de Datos e Inteligencia Artificial**, en el marco del Trabajo Final de Minería de Datos.

---

## 📌 Características principales del dashboard

### ✔ Autenticación de Usuarios  
- Sistema de login con *streamlit-authenticator*.  
- Roles:  
  - **Administrador** (acceso ampliado)  
  - **Invitado** (acceso limitado)  
- Página oculta exclusiva para administradores.

### ✔ Visualizaciones Interactivas  
- Análisis de Recursos Humanos por:  
  - Dependencias  
  - Regiones  
  - Jerarquías  
- Análisis de armamento según estado operativo.

### ✔ Mapa Geográfico de Dependencias  
- Construido con **Folium** y mostrado en Streamlit con **streamlit-folium**.  
- Muestra la ubicación aproximada de cada dependencia policial de la provincia.

### ✔ Generación de Reportes PDF  
- PDF institucional descargable.  
- Incluye KPIs clave:  
  - Total de personal  
  - Cantidad de dependencias  
  - Armamento registrado

### ✔ Anonimización del Dataset  
- Se anonimiza el personal mediante un **hash SHA-256**,  
  reemplazando nombres por un identificador seguro e irreversible.  
- Cumple con requisitos de protección de datos sensibles.

---

## 🧠 Tecnologías utilizadas

| Categoría | Herramientas |
|----------|--------------|
| Lenguaje | Python 3.x |
| Dashboard | Streamlit |
| Visualizaciones | Plotly, Folium |
| PDF | reportlab |
| Seguridad | streamlit-authenticator |
| Procesamiento de datos | Pandas, NumPy |
| Control de versiones | Git + GitHub |
| Entorno de análisis | Google Colab |

---

## 📁 Estructura del Proyecto

/
├── app/
│ ├── app.py
│ ├── requirements.txt
│
├── data/
│ ├── armamento.csv
│ ├── rrhh_dependencias.csv
│
├── docs/
│ ├── G6_Informe PP2_SedeCentral.pdf
│
├── notebooks/
│ └── g6_pp3_analisis_completo.ipynb
│
│── README.md

---

## 🚀 Ejecución local del dashboard

### 1️⃣ Clonar este repositorio
git clone https://github.com/usuario/dashboard-policial.git
cd dashboard-policial

2️⃣ Instalar dependencias
pip install -r requirements.txt

3️⃣ Ejecutar Streamlit
streamlit run app.py 

### ☁️ Despliegue en Streamlit Cloud
- 1. Subir el repositorio a GitHub.
- 2. Ir a: https://share.streamlit.io
- 3. Seleccionar el repositorio y rama.
- 4. Elegir app.py como archivo principal.
- 5. Agregar requirements.txt.
La app estará disponible en una URL pública para presentación del proyecto.

## 🚀 Dashboard Interactivo (Streamlit)
El dashboard del proyecto ya se encuentra desplegado en línea:
👉 https://dashboard-dcgc-apzexjm5x5mcxumhyrdw2m.streamlit.app/


### 🔐 Notas sobre Seguridad y Privacidad
- Este dashboard implementa:
- Anonimización mediante hash SHA-256
- Separación de roles
- Página oculta para administración
- No expone información personal identificable

### 👥 Equipo de desarrollo
Grupo 6 – Tecnicatura en Ciencia de Datos e Inteligencia Artificial
- Andrade, Miguel Enrique.
- Coronel, Atilio Maximiliano.
- Gimenez, Roberto David.
- Jimenez, Javier Oscar.
- Rios Santillan, Melany Ayelen.
- Docente: Mubarqui Fernando

## 🎥 Presentación Final

[![Video Demo](https://img.youtube.com/vi/-6hmsZqvydU/0.jpg)](https://www.youtube.com/watch?v=-6hmsZqvydU)

👉 Haz clic en la imagen para ver el video completo de la demo técnica.


📚 Licencia
Este proyecto se distribuye con fines educativos.
Uso no autorizado para entornos sensibles está prohibido.
