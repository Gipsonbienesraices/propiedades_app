import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def create_tables():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        
        print("Conectado a la base de datos PostgreSQL")
        
        # Crear tabla de propiedades
        cur.execute('''
            CREATE TABLE IF NOT EXISTS propiedades (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                precio REAL NOT NULL,
                ubicacion TEXT NOT NULL,
                descripcion TEXT,
                recamaras INTEGER,
                banos INTEGER,
                tipo_propiedad TEXT NOT NULL,
                operacion TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL
            )
        ''')
        print("✓ Tabla 'propiedades' creada/verificada")
        
        # Crear tabla de imágenes
        cur.execute('''
            CREATE TABLE IF NOT EXISTS imagenes (
                id SERIAL PRIMARY KEY,
                propiedad_id INTEGER NOT NULL,
                ruta TEXT NOT NULL,
                FOREIGN KEY (propiedad_id) REFERENCES propiedades (id)
            )
        ''')
        print("✓ Tabla 'imagenes' creada/verificada")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n✅ Migración completada exitosamente!")
        print("Las tablas han sido creadas en la base de datos PostgreSQL.")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        raise

if __name__ == '__main__':
    create_tables()
