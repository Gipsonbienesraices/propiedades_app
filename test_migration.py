import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {DATABASE_URL[:20]}...")  # Solo muestra los primeros caracteres por seguridad

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✓ Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print(f"✗ Error de conexión: {e}")
