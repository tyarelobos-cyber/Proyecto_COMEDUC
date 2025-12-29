from supabase import create_client

# 1. Tus datos de Supabase (Pégalos aquí)
url_proyecto = "https://hclgbqmpxnyerxbxaozm.supabase.co"
llave_anon = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhjbGdicW1weG55ZXJ4Ynhhb3ptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0MjU1MDIsImV4cCI6MjA4MjAwMTUwMn0.W5vN_pt190k5D2Z6cTzsrB52weIbW-xNBghECJ39aTU"

# 2. Intentar la conexión
try:
    supabase = create_client(url_proyecto, llave_anon)
    print(" ¡Increíble! Python se conectó exitosamente a Supabase.")
    
    # Vamos a probar leer la tabla de instituciones que creamos antes
    respuesta = supabase.table("instituciones").select("*").execute()
    print("Conexión verificada. La tabla instituciones está lista.")

except Exception as e:
    print(f" Hubo un error al conectar: {e}")