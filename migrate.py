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
                fecha_creacion TEXT NOT NULL,
                youtube_url TEXT
            )
        ''')
        print("✓ Tabla 'propiedades' creada/verificada")
        
        # Agregar columna youtube_url si no existe (para tablas existentes)
        try:
            cur.execute('ALTER TABLE propiedades ADD COLUMN IF NOT EXISTS youtube_url TEXT')
            print("✓ Columna 'youtube_url' agregada a tabla 'propiedades'")
        except Exception as e:
            print(f"  (La columna ya existe o error: {e})")
        
        # Crear tabla de imágenes con URLs externas
        cur.execute('''
            CREATE TABLE IF NOT EXISTS imagenes (
                id SERIAL PRIMARY KEY,
                propiedad_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                es_principal BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (propiedad_id) REFERENCES propiedades (id)
            )
        ''')
        print("✓ Tabla 'imagenes' creada/verificada")
        
        # Migrar datos existentes si es necesario
        try:
            # Verificar si la columna 'ruta' existe y renombrarla a 'url'
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'imagenes' AND column_name = 'ruta'")
            if cur.fetchone():
                cur.execute('ALTER TABLE imagenes RENAME COLUMN ruta TO url')
                print("✓ Columna 'ruta' renombrada a 'url' en tabla 'imagenes'")
        except Exception as e:
            print(f"  (Migración de columnas: {e})")
        
        # Agregar columna es_principal si no existe
        try:
            cur.execute('ALTER TABLE imagenes ADD COLUMN IF NOT EXISTS es_principal BOOLEAN DEFAULT FALSE')
            print("✓ Columna 'es_principal' agregada a tabla 'imagenes'")
        except Exception as e:
            print(f"  (La columna ya existe o error: {e})")
        
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
