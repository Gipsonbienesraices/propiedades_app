# Sistema de Autenticación - Instrucciones de Uso

## 🔐 Seguridad Implementada

He implementado un sistema completo de autenticación que protege todas las funciones de administración.

## ✅ Características de Seguridad

### **Para visitantes públicos:**
- ✅ Solo pueden ver el catálogo de propiedades
- ✅ No ven botones de "Registrar Propiedad"
- ✅ No ven opciones de "Editar" o "Eliminar"
- ✅ Acceso de solo lectura

### **Para administradores (autenticados):**
- ✅ Pueden registrar nuevas propiedades
- ✅ Pueden editar propiedades existentes
- ✅ Pueden eliminar propiedades
- ✅ Pueden gestionar imágenes (agregar/eliminar)
- ✅ Ven su nombre de usuario en la navegación

## 🔑 Credenciales de Acceso

**Usuario por defecto:**
- **Usuario:** `admin`
- **Contraseña:** `admin123`

⚠️ **IMPORTANTE:** Las credenciales por defecto están ocultas en la interfaz por seguridad. Debes cambiar la contraseña inmediatamente después del primer inicio de sesión.

## 🚀 Cómo Usar el Sistema

### 1. Acceso Público (Visitantes)
Los visitantes pueden:
- Navegar por https://tu-url-render.onrender.com
- Ver todas las propiedades con imágenes
- Ver detalles de cada propiedad
- Usar el carrusel de imágenes

**NO pueden:**
- Registrar propiedades
- Editar propiedades
- Eliminar propiedades
- Acceder al panel de administración

### 2. Acceso Administrativo
Para administrar propiedades:

1. **Iniciar Sesión:**
   - Click en "Iniciar Sesión" en la navegación superior
   - Usuario: `admin`
   - Contraseña: `admin123`
   - Click en "Iniciar Sesión"

2. **Cambiar Contraseña (PRIMER PASO RECOMENDADO):**
   - Después de iniciar sesión, click en "Cambiar Contraseña" en la navegación
   - Ingresa tu contraseña actual: `admin123`
   - Ingresa tu nueva contraseña (mínimo 6 caracteres)
   - Confirma la nueva contraseña
   - Click en "Cambiar Contraseña"
   - ¡Listo! Tu contraseña ha sido actualizada de forma segura

2. **Funciones Disponibles:**
   - **Registrar Propiedad:** Click en "Registrar Nueva Propiedad"
   - **Editar Propiedad:** Click en "Editar" en cada tarjeta de propiedad
   - **Eliminar Propiedad:** Click en "Eliminar" con confirmación
   - **Gestionar Imágenes:** Agregar nuevas imágenes o eliminar existentes

3. **Cerrar Sesión:**
   - Click en "Cerrar Sesión (admin)" en la navegación superior

## 🔄 Cambios Realizados

### **Archivos Modificados:**
- <ref_file file="C:\Users\USER\propiedades_app\app.py" /> - Sistema de autenticación completo
- <ref_file file="C:\Users\USER\propiedades_app\requirements.txt" /> - Flask-Login agregado
- <ref_file file="C:\Users\USER\propiedades_app\migrate.py" /> - Tabla de usuarios creada
- <ref_file file="C:\Users\USER\propiedades_app\start.sh" /> - Instalación automática de dependencias
- <ref_file file="C:\Users\USER\propiedades_app\templates\index.html" /> - Botones condicionales
- <ref_file file="C:\Users\USER\propiedades_app\templates\registrar.html" /> - Protegido con login
- <ref_file file="C:\Users\USER\propiedades_app\templates\login.html" /> - Nueva página de login
- <ref_file file="C:\Users\USER\propiedades_app\templates\editar.html" /> - Nueva página de edición

### **Base de Datos:**
- Nueva tabla `usuarios` con campos:
  - `id` (PRIMARY KEY)
  - `username` (UNIQUE)
  - `password_hash` (encriptado)
  - `is_admin` (BOOLEAN)

## 🛡️ Seguridad Adicional

### **Protección de Rutas:**
- `/registrar` - Requiere login
- `/editar/<id>` - Requiere login
- `/eliminar/<id>` - Requiere login (POST)
- `/logout` - Requiere login
- `/cambiar_password` - Requiere login

### **Encriptación:**
- Contraseñas almacenadas con `werkzeug.security.generate_password_hash`
- Verificación con `werkzeug.security.check_password_hash`
- Cambio de contraseña seguro con verificación de contraseña actual

### **Sesiones:**
- Gestión de sesiones con Flask-Login
- `login_required` decorator para protección
- Redirección automática a login si no está autenticado

### **Gestión de Archivos:**
- La carpeta `imagenes_propiedades` se crea automáticamente si no existe
- Esto soluciona el error `FileNotFoundError` en el servidor de Render
- Los nombres de archivos incluyen timestamp para evitar duplicados

## 🔧 Soluciones Implementadas

### **Problema de Carpeta de Imágenes:**
- **Error Original:** `FileNotFoundError: [Errno 2] No such file or directory: 'imagenes_propiedades/...'`
- **Solución:** El código ahora verifica si la carpeta existe y la crea automáticamente con `os.makedirs()`
- **Resultado:** Ya no habrá errores al subir imágenes en el servidor de Render

### **Seguridad de Contraseñas:**
- **Problema Original:** Credenciales visibles en la página de login
- **Solución:** Credenciales ocultas de la interfaz pública
- **Funcionalidad Nueva:** Sistema para cambiar contraseña de forma segura
- **Resultado:** Mayor seguridad para los administradores

### **Crear Múltiples Usuarios:**
Puedes agregar más usuarios administradores desde la base de datos o crear una interfaz de gestión de usuarios.

## 🎯 Verificación

Después del deploy en Render:

1. **Acceso Público:**
   - Abre tu URL pública
   - Verifica que NO veas botones de administración
   - Solo deberías ver el catálogo

2. **Acceso Admin:**
   - Inicia sesión con admin/admin123
   - Verifica que APAREZCAN los botones de administración
   - **IMPORTANTE:** Click en "Cambiar Contraseña" y actualiza tu contraseña
   - Prueba registrar, editar y eliminar propiedades
   - Verifica que las imágenes se guarden correctamente (sin error de carpeta)
   - Cierra sesión y verifica que desaparezcan los botones

## ⚠️ Notas Importantes

- La migración (`migrate.py`) creará automáticamente el usuario admin
- Render instalará Flask-Login automáticamente durante el deploy
- Las sesiones se gestionan de forma segura con cookies
- El sistema es escalable para agregar más usuarios en el futuro

¡Tu aplicación ahora está completamente protegida con autenticación!