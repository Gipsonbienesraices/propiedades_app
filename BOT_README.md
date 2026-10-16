# Bot de Facebook - Documentación

## ⚠️ ADVERTENCIA IMPORTANTE

Este bot utiliza técnicas de scraping en Facebook, lo cual puede violar los términos de servicio de la plataforma. El uso es bajo tu propio riesgo y responsabilidad.

## 🏗️ Arquitectura Modular

El bot está organizado en la carpeta `bot_services/` para no interferir con la aplicación web principal:

```
bot_services/
├── __init__.py          # Exportaciones del módulo
├── config.py            # Configuración centralizada
├── scraper.py           # Facebook Scraper con Playwright-Stealth
├── lead_extractor.py    # Clasificador de leads
├── matchmaker.py        # Motor de emparejamiento
├── commenter.py         # Auto-comentarios con límites
├── database.py          # Gestor de base de datos
└── state.json           # Sesión de Facebook (cookies)
```

## 🔧 Configuración Requerida

### 1. Variables de Entorno (.env)

```bash
# Base de datos para el bot
BOT_DATABASE_URL=postgresql://usuario:password@host:5432/base_datos

# Telegram para alertas
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id

# Tu número de teléfono
MY_PHONE_NUMBER=0987654321

# Habilitar bot
BOT_ENABLED=false  # Cambiar a true para activar
```

### 2. Base de Datos en la Nube

El bot requiere PostgreSQL en la nube (Supabase o Neon) para evitar la volatilidad de Render.

**Opciones:**
- **Supabase:** Gratis, PostgreSQL, fácil configuración
- **Neon:** Serverless PostgreSQL, ideal para serverless

### 3. Playwright

Instalar dependencias:
```bash
pip install playwright
playwright install chromium
```

## 🚀 Funcionalidades

### 1. Scraping con Stealth
- Playwright con playwright-stealth
- Carga de sesión desde state.json
- Desactivación de imágenes para optimizar memoria
- Scroll gradual imperfecto
- Pausas aleatorias largas (1-3 minutos)

### 2. Clasificación de Leads
- Comprador vs Vendedor
- Busca Arriendo vs Ofrece Arriendo
- Extracción de sector, presupuesto, teléfonos
- Filtro de antigüedad (máximo 16 semanas)

### 3. Emparejamiento
- Cruza demanda con oferta
- Coincidencia por sector y presupuesto
- Alertas por Telegram

### 4. Auto-Comentarios
- Límite: 1 comentario cada 45 minutos
- Máximo: 10 comentarios diarios
- Spintax para mensajes variados
- Solo en leads de compradores

## 🛡️ Medidas de Seguridad

1. **Pausas aleatorias largas** entre búsquedas
2. **Scroll gradual imperfecto** para simular humano
3. **Límites estrictos** de comentarios
4. **Carga de sesión** para evitar login repetido
5. **Comentarios desactivados** inicialmente por seguridad

## 📊 Gestión de Memoria

- **Cierre inmediato** del navegador después de scraping
- **Desactivación de carga de imágenes**
- **Ejecución en segundo plano** con APScheduler
- **Ciclos programados** cada 4 horas

## 🚦 Estados del Bot

### Inicial (Desactivado)
- `BOT_ENABLED=false` en .env
- Bot no se ejecuta
- Aplicación web funciona normalmente

### Activo
- `BOT_ENABLED=true` en .env
- Bot se ejecuta cada 4 horas
- Logs en consola de Render

## 🐛 Debugging

Logs en Render mostrarán:
- `🤖 Iniciando ciclo del bot...`
- `🔍 Ejecutando scraping completo...`
- `📊 Simulando procesamiento de posts...`
- `🔗 Ejecutando matchmaking...`
- `💬 Ejecutando comentarios...`

## ⚡ Activación/Desactivación

Para activar el bot:
1. Configurar variables de entorno
2. Cambiar `BOT_ENABLED=true` en .env
3. Hacer deploy a Render
4. Verificar logs para confirmar ejecución

Para desactivar:
1. Cambiar `BOT_ENABLED=false` en .env
2. Hacer deploy

## 📞 Soporte Telegram

Para recibir alertas de matches:
1. Crear bot en @BotFather
2. Obtener TOKEN
3. Obtener CHAT_ID (usando @userinfobot)
4. Configurar en .env

## 🔒 Archivos Sensibles

- `bot_services/state.json` - Sesión de Facebook (NO subir a Git)
- `.env` - Variables de entorno (NO subir a Git)
- `BOT_DATABASE_URL` - URL de base de datos del bot

## 🚨 Riesgos

1. **Bloqueo de cuenta de Facebook**
2. **Violación de Términos de Servicio**
3. **Detección por sistemas anti-bot**
4. **Problemas legales**

**El uso es exclusivamente bajo tu responsabilidad.**
