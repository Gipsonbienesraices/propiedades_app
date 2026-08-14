# Instrucciones de Despliegue - Propiedades App

Sigue estos pasos para desplegar tu aplicación en internet.

## 📋 PASO 1: Subir código a GitHub

### 1.1 Crear repositorio en GitHub
1. Ve a [https://github.com](https://github.com)
2. Inicia sesión con tu cuenta
3. Click en el botón "+" (arriba a la derecha) → "New repository"
4. Nombre del repositorio: `propiedades_app`
5. Marca "Public" o "Private" según tu preferencia
6. Click en "Create repository"

### 1.2 Subir el código desde tu computadora
Abre una terminal en la carpeta `C:\Users\USER\propiedades_app` y ejecuta:

```bash
git init
git add .
git commit -m "Initial commit - Sistema de propiedades con PostgreSQL"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/propiedades_app.git
git push -u origin main
```

**Importante:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

---

## 🗄️ PASO 2: Configurar Base de Datos PostgreSQL

### Opción A: Usar Render (Recomendado - Gratis)
1. Ve a [https://render.com](https://render.com)
2. Crea una cuenta gratuita
3. Click en "New +" → "PostgreSQL"
4. Nombre: `propiedades-db`
5. Database: `propiedades`
6. User: `propiedades_user`
7. Region: Selecciona la más cercana a ti
8. Click en "Create Database"
9. Espera a que la base de datos esté lista
10. Copia la "Internal Database URL" (la necesitarás más tarde)

### Opción B: Usar Supabase (Alternativa - Gratis)
1. Ve a [https://supabase.com](https://supabase.com)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto llamado "propiedades"
4. Ve a Settings → Database
5. Copia la "Connection String" (la necesitarás más tarde)

---

## 🚀 PASO 3: Desplegar en Render

### 3.1 Conectar GitHub con Render
1. En [https://render.com](https://render.com), ve a tu dashboard
2. Click en "New +" → "Web Service"
3. Click en "Connect GitHub"
4. Autoriza a Render para acceder a tu cuenta de GitHub
5. Busca y selecciona el repositorio `propiedades_app`
6. Click en "Connect"

### 3.2 Configurar el Web Service
Render detectará automáticamente el archivo `render.yaml`. Configurará:
- Nombre: `propiedades-app`
- Environment: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### 3.3 Configurar Variables de Entorno
Si Render no detecta automáticamente el archivo `render.yaml`, agrega manualmente:

1. En la sección "Environment", agrega:
   - **Key**: `DATABASE_URL`
   - **Value**: La URL que copiaste en el PASO 2
   - **Key**: `SECRET_KEY`
   - **Value**: Genera una clave aleatoria (puedes usar: https://randomkeygen.com/)

### 3.4 Desplegar
1. Click en "Create Web Service"
2. Render comenzará a construir y desplegar tu aplicación
3. Espera unos minutos (puede tardar 5-10 minutos la primera vez)
4. Cuando termine, verás una URL pública como: `https://propiedades-app.onrender.com`

---

## ✅ PASO 4: Verificar el Despliegue

1. Abre la URL que te proporcionó Render
2. Deberías ver la página principal de tu aplicación
3. Intenta registrar una propiedad de prueba
4. Verifica que las imágenes se carguen correctamente

---

## 🔧 Solución de Problemas

### Error: "No module named 'psycopg2'"
El archivo `render.yaml` debería instalar automáticamente las dependencias. Si no, verifica que `requirements.txt` contenga `psycopg2-binary==2.9.9`.

### Error: "Database connection failed"
Verifica que la variable `DATABASE_URL` esté correctamente configurada en Render.

### Las imágenes no se cargan
Verifica que la carpeta `imagenes_propiedades` tenga permisos de escritura en el servidor.

### Error: "Table doesn't exist"
La aplicación debería crear las tablas automáticamente. Si no, puedes necesitar acceder a la base de datos directamente en Render y ejecutar el SQL del archivo `app.py`.

---

## 📝 Notas Adicionales

- La base de datos PostgreSQL en Render tiene un plan gratuito con límites
- Para desarrollo local, puedes usar PostgreSQL localmente o volver a SQLite temporalmente
- La aplicación está configurada para usar Gunicorn como servidor de producción
- Render reiniciará automáticamente tu aplicación si hay errores

---

## 🎯 ¡Listo!

Tu aplicación de propiedades debería estar ahora accesible desde internet con URL pública, base de datos PostgreSQL, y sistema de carga de imágenes funcionando.