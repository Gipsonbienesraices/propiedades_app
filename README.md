# Sistema de Registro de Propiedades

Aplicación web para registrar propiedades inmobiliarias con imágenes. Configurada para despliegue en Render con PostgreSQL.

## Características

- Registro de propiedades con los siguientes campos:
  - Título
  - Precio
  - Ubicación
  - Descripción
  - Recámaras (opcional para terrenos)
  - Baños (opcional para terrenos)
  - Tipo de Propiedad (Casa, Departamento, Terreno)
  - Operación (fijo en Venta)
  - Múltiples imágenes

- Lógica inteligente:
  - Cuando se selecciona "Terreno", los campos de Recámaras y Baños se ocultan automáticamente
  - La operación siempre es "Venta" (sin opción de renta)

- Almacenamiento:
  - Datos en base de datos PostgreSQL
  - Imágenes en sistema de archivos del servidor

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/propiedades_app.git
cd propiedades_app
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tu configuración de base de datos PostgreSQL
```

5. Ejecutar la aplicación:
```bash
python app.py
```

6. Abrir el navegador en:
```
http://127.0.0.1:5000
```

## Despliegue en Render

### Paso 1: Crear repositorio en GitHub
1. Ve a [GitHub](https://github.com) y crea un nuevo repositorio llamado `propiedades_app`
2. Sube el código a GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/propiedades_app.git
git push -u origin main
```

### Paso 2: Desplegar en Render
1. Ve a [Render](https://render.com) y crea una cuenta
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Click en "Create Web Service"
6. Render creará automáticamente:
   - Base de datos PostgreSQL
   - Servidor web con Gunicorn
   - Variables de entorno necesarias

### Paso 3: Configurar base de datos
1. En Render, ve a la sección "Databases"
2. Copia la "Internal Database URL"
3. Ve a tu Web Service → "Environment"
4. La variable `DATABASE_URL` ya estará configurada automáticamente por el archivo `render.yaml`

## Uso

1. **Registrar Propiedad**: Click en "Registrar Nueva Propiedad"
2. **Completar formulario**:
   - Tipo de Propiedad: Seleccionar Casa, Departamento o Terreno
   - Si seleccionas Terreno, los campos de Recámaras y Baños se ocultan
   - La Operación siempre será Venta
   - Puedes subir múltiples imágenes
3. **Ver propiedades**: En la página principal verás todas las propiedades registradas con carrusel de imágenes

## Estructura del Proyecto

```
propiedades_app/
├── app.py                      # Aplicación Flask principal
├── requirements.txt            # Dependencias
├── Procfile                    # Configuración de proceso para Render
├── runtime.txt                 # Versión de Python
├── render.yaml                 # Configuración completa de Render
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos ignorados por Git
├── imagenes_propiedades/      # Carpeta para imágenes (ignorada en Git)
├── static/                    # Archivos estáticos
├── templates/                 # Plantillas HTML
│   ├── index.html            # Página principal
│   └── registrar.html        # Formulario de registro
└── README.md                 # Este archivo
```

## Tecnologías

- Backend: Flask (Python)
- Base de datos: PostgreSQL
- Servidor de producción: Gunicorn
- Plataforma de despliegue: Render
- Frontend: HTML + Bootstrap 5
- Almacenamiento de archivos: Sistema de archivos del servidor

## Variables de Entorno

- `DATABASE_URL`: URL de conexión a PostgreSQL (Render la configura automáticamente)
- `SECRET_KEY`: Clave secreta para Flask (Render la genera automáticamente)

## Notas Importantes

- La base de datos SQLite local ha sido reemplazada por PostgreSQL para producción
- Las imágenes se almacenan en el sistema de archivos del servidor (no en base de datos)
- Para desarrollo local, necesitas una instancia de PostgreSQL o configurar SQLite localmente
