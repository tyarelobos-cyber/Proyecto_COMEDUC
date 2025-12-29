import pandas as pd
from supabase import create_client

# 1. Conexión
url = "https://hclgbqmpxnyerxbxaozm.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhjbGdicW1weG55ZXJ4Ynhhb3ptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0MjU1MDIsImV4cCI6MjA4MjAwMTUwMn0.W5vN_pt190k5D2Z6cTzsrB52weIbW-xNBghECJ39aTU"
supabase = create_client(url, key)

# 2. Leer Excel saltando las primeras 12 filas (donde están los nombres de las columnas reales)
# Usamos 'skiprows=12' para llegar directo a los datos
df = pd.read_csv("tu_archivo.csv", skiprows=12) 

# 3. Limpieza: Eliminamos la columna de nombres para proteger la privacidad
df_anonimo = df.drop(columns=['Nombre del Estudiante', 'Número de Lista'])

# 4. Calcular el Promedio del Curso (Tu KPI de RQF02)
# Convertimos los textos con coma (ej: "58,33") a números reales
for col in df_anonimo.columns:
    df_anonimo[col] = df_anonimo[col].str.replace(',', '.').astype(float)

promedio_curso = df_anonimo.mean().mean() # Promedio general de todos los OA
categoria_final = "Satisfactorio" if promedio_curso >= 60 else "Insatisfactorio"

# 5. Subir el resultado AGREGADO a Supabase
datos_kpi = {
    "id_institucion": 1, # ID del Liceo Felisa
    "nombre_curso": "I A (HC-310)",
    "puntaje_promedio": round(promedio_curso, 2),
    "categoria": categoria_final,
    "tipo_evaluacion": "Matemática - Diagnóstico 2025"
}

try:
    supabase.table("kpis").insert(datos_kpi).execute()
    print(f" Éxito: Curso I A procesado con {promedio_curso}% ({categoria_final})")
except Exception as e:
    print(f" Error: {e}")