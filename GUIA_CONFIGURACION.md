# 🎯 Guía Completa de Configuración del Bot

## PASO 1: Configurar Supabase (Base de Datos en la Nube)

### 1.1 Crear Cuenta en Supabase

1. **Ir a:** [https://supabase.com](https://supabase.com)
2. **Hacer clic en:** "Start your project"
3. **Iniciar sesión:** Con GitHub, Google o email
4. **Crear organización:** Nombre tu organización (ej: "Gipson Bienes Raíces")

### 1.2 Crear Proyecto

1. **Hacer clic en:** "New Project"
2. **Nombre del proyecto:** `propiedades-bot` (o el que prefieras)
3. **Contraseña de base de datos:** 
   - **IMPORTANTE:** Guárdala en lugar seguro
   - Debe ser segura (mínimo 12 caracteres)
4. **Región:** Selecciona "Southeast Asia (Singapore)" o "US East"
5. **Plan:** "Free" (gratuito)
6. **Hacer clic en:** "Create new project"

### 1.3 Esperar Creación (2-3 minutos)

Supabase creará automáticamente:
- Base de datos PostgreSQL
- API Keys
- Autenticación

### 1.4 Obtener BOT_DATABASE_URL

1. **En el dashboard de Supabase:**
   - Ir a: Settings → Database
   - Buscar: "Connection string"
   - Copiar la "URI" completa

2. **Formato esperado:**
   ```
   postgresql://postgres:[contraseña]@[proyecto].[region].supabase.co:5432/postgres
   ```

3. **Ejemplo real:**
   ```
   postgresql://postgres:tu_contraseña_segura@abc123.us-east-1.supabase.co:5432/postgres
   ```

**GUARDA ESTA URL** - la necesitarás para Render

---

## PASO 2: Configurar Telegram (Opcional pero Recomendado)

### 2.1 Crear Bot en Telegram

1. **Abrir Telegram** y buscar: [@BotFather](https://t.me/BotFather)
2. **Enviar comando:** `/newbot`
3. **Nombre del bot:** `GipsonPropiedadesBot` (o similar)
4. **Usuario del bot:** `gipson_propiedades_bot` (debe terminar en "bot")
5. **BotFather te dará:** `TELEGRAM_BOT_TOKEN` (guárdalo)

### 2.2 Obtener Chat ID

1. **Buscar:** [@userinfobot](https://t.me/userinfobot)
2. **Enviar cualquier mensaje** al bot
3. **Responderá con:** tu `Chat ID` (número largo)
4. **GUARDA** este número como `TELEGRAM_CHAT_ID`

---

## PASO 3: Configurar Variables en Render

### 3.1 Acceder a tu proyecto en Render

1. **Ir a:** [https://dashboard.render.com](https://dashboard.render.com)
2. **Buscar tu servicio:** `propiedades-app-1`
3. **Hacer clic en:** el servicio

### 3.2 Configurar Environment Variables

1. **Ir a:** Settings → Environment
2. **Hacer clic en:** "Add Environment Variable"

### 3.3 Agregar las siguientes variables:

#### Variable 1: BOT_DATABASE_URL
- **Key:** `BOT_DATABASE_URL`
- **Value:** [La URL que obtuviste de Supabase]
- **Sync:** "No"

#### Variable 2: TELEGRAM_BOT_TOKEN (si configuraste Telegram)
- **Key:** `TELEGRAM_BOT_TOKEN`
- **Value:** [El token de BotFather]
- **Sync:** "No"

#### Variable 3: TELEGRAM_CHAT_ID (si configuraste Telegram)
- **Key:** `TELEGRAM_CHAT_ID`
- **Value:** [El Chat ID de userinfobot]
- **Sync:** "No"

#### Variable 4: MY_PHONE_NUMBER
- **Key:** `MY_PHONE_NUMBER`
- **Value:** `0987654321` (tu número real)
- **Sync:** "No"

#### Variable 5: BOT_ENABLED
- **Key:** `BOT_ENABLED`
- **Value:** `true`
- **Sync:** "No"

### 3.4 Guardar y Deploy

1. **Hacer clic en:** "Save Changes"
2. **Render detectará cambios** y comenzará deploy automático
3. **Esperar deploy** (2-3 minutos)

---

## PASO 4: Instalar Playwright en Render

### 4.1 Crear archivo build.sh

Voy a crear el archivo `build.sh` para instalar Playwright:

```bash
#!/bin/bash
pip install playwright
playwright install chromium
```

### 4.2 Configurar en Render

1. **En Settings → Build & Deploy**
2. **En "Build Command":** `pip install -r requirements.txt && bash build.sh`
3. **Crear archivo `build.sh`** con el contenido anterior

---

## PASO 5: Verificar Funcionamiento

### 5.1 Revisar Logs en Render

1. **Ir a:** Logs → "deploy"
2. **Buscar logs que digan:**
   - "Bot programado para ejecutarse cada 4 horas"
   - "Iniciando ciclo del bot..."
   - Si hay errores, los verás en rojo

### 5.2 Verificar Tablas en Supabase

1. **En Supabase:**
   - Ir a: Table Editor
   - Deberías ver tablas: `demanda`, `oferta`, `matches`, `comentarios`

---

## ⚠️ IMPORTANTE - Seguridad

1. **NO compartas** tu BOT_DATABASE_URL
2. **NO compartas** tu TELEGRAM_BOT_TOKEN
3. **GUARDA** tu contraseña de Supabase en lugar seguro
4. **Cambia** tu contraseña de Facebook regularmente

---

## 🚨 Si algo falla

### Error: "Module not found: playwright"
- **Solución:** Revisar que `build.sh` se ejecuta correctamente en Render

### Error: "Connection refused" (Supabase)
- **Solución:** Verifica que la URL sea correcta y la contraseña de Supabase

### Error: "Bot no se ejecuta"
- **Solución:** Verifica que `BOT_ENABLED=true` en Render

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas en algún paso específico:
1. **Dime en qué paso estás atascado**
2. **Describe el error exacto**
3. **Te ayudaré a solucionarlo**
