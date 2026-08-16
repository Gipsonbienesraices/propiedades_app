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

⚠️ **IMPORTANTE:** Cambia la contraseña por defecto después del primer inicio de sesión.

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

### **Encriptación:**
- Contraseñas almacenadas con `werkzeug.security.generate_password_hash`
- Verificación con `werkzeug.security.check_password_hash`

### **Sesiones:**
- Gestión de sesiones con Flask-Login
- `login_required` decorator para protección
- Redirección automática a login si no está autenticado

## 📋 Próximos Pasos (Opcionales)

### **Cambiar Contraseña por Defecto:**
Para mayor seguridad, puedes crear una función para cambiar la contraseña:

```python
@app.route('/cambiar_password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    if request.method == 'POST':
        nueva_password = request.form['nueva_password']
        password_hash = generate_password_hash(nueva_password)
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE usuarios SET password_hash = %s WHERE id = %s', 
                   (password_hash, current_user.id))
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('index'))
    
    return render_template('cambiar_password.html')
```

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
   - Prueba registrar, editar y eliminar propiedades
   - Cierra sesión y verifica que desaparezcan los botones

## ⚠️ Notas Importantes

- La migración (`migrate.py`) creará automáticamente el usuario admin
- Render instalará Flask-Login automáticamente durante el deploy
- Las sesiones se gestionan de forma segura con cookies
- El sistema es escalable para agregar más usuarios en el futuro

¡Tu aplicación ahora está completamente protegida con autenticación!