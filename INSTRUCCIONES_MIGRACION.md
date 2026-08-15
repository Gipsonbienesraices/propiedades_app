# Instrucciones para Crear Tablas en PostgreSQL (Render)

El error "relation 'propiedades' does not exist" ocurre porque las tablas no se crearon automáticamente en la base de datos PostgreSQL. Aquí tienes 3 soluciones:

## 🎯 OPCIÓN 1: Ejecutar script localmente (MÁS FÁCIL)

### Paso 1: Obtener la URL de la base de datos de Render
1. Ve a tu dashboard de [Render](https://dashboard.render.com)
2. Entra a tu base de datos PostgreSQL
3. Copia la "Internal Database URL" (debería verse como: `postgresql://usuario:password@host:puerto/database`)

### Paso 2: Crear archivo .env local
En la carpeta `C:\Users\USER\propiedades_app`, crea un archivo llamado `.env` con:
```
DATABASE_URL=la_url_que_copiaste_de_render
SECRET_KEY=tu_clave_secreta
```

### Paso 3: Ejecutar el script de migración
```bash
cd C:\Users\USER\propiedades_app
pip install psycopg2-binary python-dotenv
python migrate.py
```

### Paso 4: Verificar
Deberías ver:
```
Conectado a la base de datos PostgreSQL
✓ Tabla 'propiedades' creada/verificada
✓ Tabla 'imagenes' creada/verificada

✅ Migración completada exitosamente!
```

---

## 🖥️ OPCIÓN 2: Usar Shell de Render

### Paso 1: Acceder al shell de tu web service
1. Ve a tu dashboard de [Render](https://dashboard.render.com)
2. Entra a tu Web Service "propiedades-app"
3. Click en "Shell" (en la parte superior)
4. Se abrirá una terminal en el navegador

### Paso 2: Ejecutar Python en el shell
```bash
python
```

### Paso 3: Ejecutar los comandos SQL
```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Crear tabla propiedades
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

# Crear tabla imagenes
cur.execute('''
    CREATE TABLE IF NOT EXISTS imagenes (
        id SERIAL PRIMARY KEY,
        propiedad_id INTEGER NOT NULL,
        ruta TEXT NOT NULL,
        FOREIGN KEY (propiedad_id) REFERENCES propiedades (id)
    )
''')

conn.commit()
conn.close()
print("Tablas creadas exitosamente")
```

### Paso 4: Salir de Python
```python
exit()
```

---

## 🔧 OPCIÓN 3: Usar PSQL de Render (MÁS TÉCNICO)

### Paso 1: Instalar PSQL localmente
Descarga e instala PostgreSQL para Windows desde [postgresql.org](https://www.postgresql.org/download/windows/)

### Paso 2: Obtener credenciales externas
1. En Render, ve a tu base de datos
2. Click en "Connections"
3. Copia la "External Database URL"

### Paso 3: Conectar y ejecutar SQL
```bash
psql "la_url_externa_que_copiaste"
```

Luego ejecuta:
```sql
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
);

CREATE TABLE IF NOT EXISTS imagenes (
    id SERIAL PRIMARY KEY,
    propiedad_id INTEGER NOT NULL,
    ruta TEXT NOT NULL,
    FOREIGN KEY (propiedad_id) REFERENCES propiedades (id)
);

\q
```

---

## 🔄 OPCIÓN 4: Modificar app.py para crear tablas automáticamente (RECOMENDADO PARA FUTURO)

Esta opción modifica el código para que las tablas se creen automáticamente cada vez que inicia la aplicación.

En `app.py`, la función `init_db()` ya debería estar configurada, pero necesitas asegurarte de que se ejecute.

Verifica que al final de `app.py` tengas:
```python
if __name__ == '__main__':
    init_db()  # Esta línea crea las tablas automáticamente
    app.run(debug=True, port=5000)
```

Para que esto funcione en Render, necesitas agregar un comando de inicio que ejecute la inicialización. Modifica el `render.yaml` o usa un script de inicio.

---

## ✅ Verificación

Después de ejecutar cualquiera de las opciones:

1. **Actualiza tu aplicación en Render** (si modificaste el código)
2. **Accede a tu URL** (ej: `https://propiedades-app.onrender.com`)
3. **El error debería desaparecer**
4. **Intenta registrar una propiedad de prueba**

---

## 🚨 Si el problema persiste

1. Verifica que la URL de la base de datos sea correcta
2. Revisa los logs en Render: Logs → Your Web Service
3. Asegúrate de que las dependencias estén instaladas: `pip install psycopg2-binary python-dotenv`

La **OPCIÓN 1** es la más sencilla si tienes acceso local a la URL de la base de datos.