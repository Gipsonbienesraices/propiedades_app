"""
Configuración del Bot de Facebook Scraper
"""

import os

class BotConfig:
    # Configuración de Facebook
    FACEBOOK_URL = "https://www.facebook.com"
    STATE_FILE = "bot_services/state.json"
    
    # Términos de búsqueda
    DEMANDA_TERMS = [
        "busco arriendo carolina",
        "busco departamento cumbayá", 
        "compro terreno sur",
        "busco casa tumbaco"
    ]
    
    OFERTA_TERMS = [
        "arriendo departamento carolina",
        "terreno en venta ecuatoriana"
    ]
    
    # Filtros de tiempo
    MAX_WEEKS_OLD = 16  # Máximo 16 semanas de antigüedad
    
    # Categorías de clasificación
    BUYER_KEYWORDS = ["busco", "compro", "presupuesto"]
    SELLER_KEYWORDS = ["vendo", "dueño directo", "en venta"]
    RENT_SEEKER_KEYWORDS = ["busco arriendo", "busco alquilar", "cerca a la usfq"]
    RENT_OFFERER_KEYWORDS = ["arriendo", "alquilo", "departamento"]
    
    # Límites de comentarios
    COMMENT_INTERVAL_MINUTES = 45  # Mínimo 45 minutos entre comentarios
    MAX_DAILY_COMMENTS = 10  # Máximo 10 comentarios diarios
    
    # Mensajes Spintax para comentarios
    COMMENT_MESSAGES = [
        "Hola, {nombre}. Vi que estás buscando {tipo}. Puedo ayudarte a encontrar opciones. Contáctame al {telefono}",
        "¡Buen día! Tengo varias opciones de {tipo} que podrían interesarte. Llámame al {telefono}",
        "Hola {nombre}, te puedo ayudar con tu búsqueda de {tipo}. Mi número es {telefono}",
        "¡Interesante! Tengo contactos para {tipo}. Avísame al {telefono}",
        "Hola, vi tu post sobre {tipo}. Tengo información útil. Llámame al {telefono}",
        "¡Buenas! Puedo asesorarte con {tipo}. Contáctame al {telefono}",
        "Hola {nombre}, te ayudo a encontrar {tipo}. Mi número: {telefono}",
        "¡Hola! Tengo excelentes opciones de {tipo}. Llámanos al {telefono}",
        "Buen día {nombre}, te puedo ayudar con {tipo}. Contáctame al {telefono}",
        "¡Hola! Para {tipo} tengo lo que necesitas. Avísame al {telefono}"
    ]
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Base de datos
    DATABASE_URL = os.getenv('BOT_DATABASE_URL', os.getenv('DATABASE_URL'))
