import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px

# 1. Configuración de la interfaz
st.set_page_config(page_title="COMEDUC BI-Metrics", layout="wide")
st.title("📊 BI-Metrics: Portal de Carga COMEDUC")
st.write("Bienvenida. Por favor, sube el reporte de la prueba DIA para comenzar el procesamiento.")

# 2. Conexión a Supabase (Asegúrate de poner tus llaves)
URL_SUPABASE = "https://hclgbqmpxnyerxbxaozm.supabase.co"
KEY_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhjbGdicW1weG55ZXJ4Ynhhb3ptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0MjU1MDIsImV4cCI6MjA4MjAwMTUwMn0.W5vN_pt190k5D2Z6cTzsrB52weIbW-xNBghECJ39aTU"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# 3. El cargador de archivos (Aquí es donde subirás el Excel después)
archivo = st.file_uploader("Selecciona el archivo Excel o CSV", type=["csv", "xlsx"])

# El código solo se ejecutará SI hay un archivo presente
if archivo is not None:
    try:
        # Leemos el archivo saltando las 12 filas de encabezado
        df = pd.read_csv(archivo, skiprows=12)
        
        # Limpieza: Quitamos nombres y mantenemos Número de Lista
        if 'Nombre del Estudiante' in df.columns:
            df = df.drop(columns=['Nombre del Estudiante'])
        
        # Limpiamos los nombres de las columnas
        df.columns = df.columns.str.strip()

        # Función para limpiar números (maneja las comas de los archivos chilenos)
        def limpiar_datos(x):
            if isinstance(x, str):
                return float(x.replace(',', '.'))
            return x

        # Identificamos las columnas de notas (las que no son el número de lista)
        columnas_notas = [c for c in df.columns if 'Lista' not in c]
        
        # Aplicamos la limpieza solo a las notas
        for col in columnas_notas:
            df[col] = df[col].apply(limpiar_datos)

        # 4. Visualización de resultados previos
        st.success("✅ Archivo cargado con éxito")
        
        promedio_curso = df[columnas_notas].mean().mean()
        st.metric("Promedio General del Curso", f"{promedio_curso:.2f}%")

        # Gráfico de barras
        fig = px.bar(df[columnas_notas].mean(), title="Logro por OA")
        st.plotly_chart(fig)

        # 5. Botón para enviar a la Base de Datos
        if st.button("🚀 Enviar datos a Supabase"):
            for _, fila in df.iterrows():
                # Calculamos el promedio del alumno
                promedio_alumno = fila[columnas_notas].mean()
                
                # Preparamos el registro para Supabase
                datos = {
                    "numero_lista": int(fila['Número de Lista']),
                    "puntaje": round(float(promedio_alumno), 2),
                    "materia": "Matemática"
                }
                supabase.table("estudiantes").insert(datos).execute()
            
            st.balloons()
            st.success("¡Datos guardados! Power BI ya puede visualizarlos.")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

# 6. Espacio para el Dashboard final
st.divider()
st.subheader("🔗 Dashboard de Power BI")
st.info("Aquí aparecerá el gráfico conectado a la base de datos.")