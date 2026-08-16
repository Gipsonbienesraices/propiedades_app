import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def create_tables():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        
        print("Conectado a la base de datos PostgreSQL")
        
        # Crear tabla de usuarios
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT TRUE
            )
        ''')
        print("✓ Tabla 'usuarios' creada/verificada")
        
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
        
        # Crear usuario admin por defecto si no existe
        cur.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not cur.fetchone():
            password_hash = generate_password_hash('admin123')  # Contraseña por defecto
            cur.execute(
                'INSERT INTO usuarios (username, password_hash, is_admin) VALUES (%s, %s, %s)',
                ('admin', password_hash, True)
            )
            print("✓ Usuario admin creado (username: admin, password: admin123)")
            print("  ⚠️  IMPORTANTE: Cambia la contraseña por defecto después del primer login")
        
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
