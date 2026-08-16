# Integración de Videos de YouTube - Instrucciones

## 🎥 Nueva Funcionalidad: Videos de YouTube

He integrado la posibilidad de agregar videos de YouTube a las propiedades. Esto permite mostrar tours virtuales sin saturar el servidor con archivos pesados.

## ✅ Características

- **Campo opcional:** Solo se agrega si el administrador desea incluir un video
- **Formatos compatibles:** Acepta diferentes formatos de URLs de YouTube
- **Reproductor integrado:** Muestra el video directamente en la tarjeta de la propiedad
- **Sin almacenamiento local:** Los videos se almacenan en los servidores de YouTube

## 🔗 Formatos de URLs de YouTube Soportados

El sistema acepta estos formatos de URLs:

1. **URL estándar:** `https://www.youtube.com/watch?v=VIDEO_ID`
2. **URL corta:** `https://youtu.be/VIDEO_ID`
3. **URL embed:** `https://www.youtube.com/embed/VIDEO_ID`
4. **URL con parámetros:** `https://www.youtube.com/watch?v=VIDEO_ID&t=10s`

El sistema extraerá automáticamente el ID del video sin importar el formato.

## 📝 Cómo Agregar un Video

### Al Registrar una Propiedad:

1. **Completa todos los campos de la propiedad**
2. **En el campo "Enlace de YouTube (Opcional)":**
   - Copia la URL del video de YouTube
   - Pégala en el campo
   - Ejemplo: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
3. **Guarda la propiedad**

### Al Editar una Propiedad:

1. **Entra en modo edición de la propiedad**
2. **Encuentra el campo "Enlace de YouTube (Opcional)"**
3. **Agrega o modifica la URL del video**
4. **Actualiza la propiedad**

## 🎯 Visualización

- **Si la propiedad tiene video:** El reproductor de YouTube aparecerá automáticamente debajo de las imágenes
- **Si no tiene video:** Solo se mostrarán las imágenes normales
- **Formato:** El reproductor tiene formato 16:9 para mejor visualización

## 💡 Consejos de Uso

### **Tipos de Videos Recomendados:**
- Tours virtuales de la propiedad
- Presentaciones de habitaciones principales
- Videos del entorno y ubicación
- Testimonios de clientes (si aplica)

### **Calidad del Video:**
- Usa videos de alta calidad (1080p recomendado)
- Videos cortos (1-3 minutos) tienen mejor rendimiento
- Asegúrate de que el audio sea claro si tiene narración

### **Configuración de YouTube:**
- El video debe ser **público** o **no listado** en YouTube
- Videos privados no se reproducirán
- Configura el video en YouTube con miniatura atractiva

## 🔧 Cambios Técnicos

### **Base de Datos:**
- Nueva columna `youtube_url` en tabla `propiedades`
- La migración se ejecuta automáticamente en el próximo deploy

### **Backend:**
- Función `extract_youtube_id()` para procesar diferentes formatos de URLs
- Almacenamiento solo del ID del video (no la URL completa)
- Validación automática del formato de URL

### **Frontend:**
- Campo opcional en formularios de registro y edición
- Reproductor integrado usando iframe de YouTube
- Diseño responsivo con Bootstrap 5

## 📊 Ejemplos de URLs

### ✅ **Formatos Válidos:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
https://www.youtube.com/embed/dQw4w9WgXcQ
https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s
```

### ❌ **Formatos No Válidos:**
```
https://www.youtube.com/watch (sin ID del video)
https://vimeo.com/123456 (otra plataforma)
archivo_local.mp4 (archivos locales)
```

## 🚀 Beneficios

1. **Sin carga al servidor:** Los videos se alojan en YouTube
2. **Fácil de usar:** Solo copiar y pegar la URL
3. **Compatibilidad:** Funciona en todos los dispositivos
4. **Atractivo visual:** Mejora la presentación de propiedades
5. **Profesional:** Demuestra compromiso con la calidad

## ⚠️ Notas Importantes

- El campo es completamente opcional
- Las propiedades sin video funcionan normalmente
- La URL se valida y procesa automáticamente
- Solo se almacena el ID del video para eficiencia
- Los videos deben estar configurados como públicos en YouTube

## 🎯 Próximas Mejoras (Opcionales)

- Configuración de inicio automático del video
- Control de volumen predeterminado
- Soporte para otras plataformas (Vimeo, etc.)
- Galería de múltiples videos por propiedad

¡La integración de YouTube hace que tu catálogo de propiedades sea mucho más dinámico y atractivo!