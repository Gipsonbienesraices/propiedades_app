"""
Facebook Scraper con Playwright-Stealth
Optimizado para uso responsable y con medidas de seguridad
"""

import asyncio
import random
import time
import json
import os
import re
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from .config import BotConfig

class FacebookScraper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.config = BotConfig()
        
    async def init_browser(self):
        """Inicializar navegador con configuración stealth y optimización de memoria"""
        playwright = await async_playwright().start()
        
        # Configuración optimizada para memoria
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Cargar estado desde archivo si existe
        if os.path.exists(self.config.STATE_FILE):
            with open(self.config.STATE_FILE, 'r') as f:
                state = json.load(f)
                await self.context.add_cookies(state['cookies'])
                await self.context.set_geolocation(state.get('geolocation', {}))
        
        self.page = await self.context.new_page()
        
        # Aplicar stealth
        await stealth_async(self.page)
        
        # Desactivar carga de imágenes para optimizar memoria
        await self.page.route("**/*.{png,jpg,jpeg,gif,webp}", lambda route: route.abort())
        
        print("✓ Navegador inicializado con configuración stealth")
        
    async def save_state(self):
        """Guardar estado del navegador (cookies, etc.)"""
        state = {
            'cookies': await self.context.cookies(),
            'geolocation': await self.context.geolocation()
        }
        with open(self.config.STATE_FILE, 'w') as f:
            json.dump(state, f)
        print("✓ Estado guardado")
        
    async def gradual_scroll(self, max_scrolls=5):
        """Scroll gradual imperfecto para simular comportamiento humano"""
        for i in range(max_scrolls):
            # Scroll aleatorio entre 300-700 pixels
            scroll_amount = random.randint(300, 700)
            await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            
            # Pausa aleatoria entre 2-5 segundos
            await asyncio.sleep(random.uniform(2, 5))
            
            # Pequeño scroll hacia arriba ocasionalmente (comportamiento humano)
            if random.random() < 0.2:
                await self.page.evaluate(f"window.scrollBy(0, -{random.randint(50, 150)})")
                await asyncio.sleep(random.uniform(1, 2))
    
    async def random_pause(self, min_minutes=1, max_minutes=3):
        """Pausa aleatoria larga entre búsquedas"""
        pause_seconds = random.uniform(min_minutes * 60, max_minutes * 60)
        print(f"⏸️ Pausa aleatoria de {pause_seconds/60:.1f} minutos")
        await asyncio.sleep(pause_seconds)
    
    def is_within_max_weeks(self, post_date_str):
        """Verificar si el post está dentro del límite de 16 semanas"""
        try:
            # Parsear diferentes formatos de fecha de Facebook
            post_date = self.parse_facebook_date(post_date_str)
            if not post_date:
                return False
                
            max_date = datetime.now() - timedelta(weeks=self.config.MAX_WEEKS_OLD)
            return post_date >= max_date
        except Exception as e:
            print(f"Error al procesar fecha: {e}")
            return False
    
    def parse_facebook_date(self, date_str):
        """Parsear diferentes formatos de fecha de Facebook"""
        # Implementación simplificada - en producción sería más compleja
        now = datetime.now()
        
        if "hace" in date_str.lower():
            # "hace 2 horas", "hace 1 día", etc.
            if "hora" in date_str.lower():
                hours = int(re.search(r'\d+', date_str).group())
                return now - timedelta(hours=hours)
            elif "día" in date_str.lower() or "dia" in date_str.lower():
                days = int(re.search(r'\d+', date_str).group())
                return now - timedelta(days=days)
            elif "semana" in date_str.lower():
                weeks = int(re.search(r'\d+', date_str).group())
                return now - timedelta(weeks=weeks)
            elif "mes" in date_str.lower():
                months = int(re.search(r'\d+', date_str).group())
                return now - timedelta(days=months*30)
        
        return None
    
    async def search_facebook(self, search_terms, phase):
        """Buscar en Facebook con términos específicos"""
        print(f"🔍 FASE {phase}: Buscando '{search_terms}'")
        
        try:
            # Navegar a Facebook
            await self.page.goto(self.config.FACEBOOK_URL)
            await asyncio.sleep(random.uniform(3, 6))
            
            # Encontrar barra de búsqueda
            search_box = await self.page.wait_for_selector('input[placeholder*="Buscar"]', timeout=10000)
            await search_box.fill(search_terms)
            await asyncio.sleep(random.uniform(1, 2))
            
            # Presionar Enter
            await search_box.press('Enter')
            await asyncio.sleep(random.uniform(3, 5))
            
            # Navegar a pestaña "Publicaciones" o "Todo"
            try:
                posts_tab = await self.page.wait_for_selector('text="Publicaciones"', timeout=5000)
                await posts_tab.click()
                await asyncio.sleep(random.uniform(2, 3))
            except:
                print("No se encontró pestaña Publicaciones, usando resultados por defecto")
            
            # Scroll gradual para cargar más resultados
            await self.gradual_scroll(max_scrolls=3)
            
            # Extraer posts
            posts = await self.extract_posts()
            
            print(f"✓ Encontrados {len(posts)} posts para '{search_terms}'")
            return posts
            
        except Exception as e:
            print(f"✗ Error en búsqueda: {e}")
            return []
    
    async def extract_posts(self):
        """Extraer información de posts de la página actual"""
        posts = []
        
        try:
            # Selectores de posts de Facebook (pueden cambiar)
            post_elements = await self.page.query_selector_all('[data-testid="story-subtitle"]')
            
            for element in post_elements:
                try:
                    # Extraer texto del post
                    post_text = await element.evaluate('el => el.parentElement.parentElement.innerText')
                    
                    # Extraer fecha
                    date_element = await element.query_selector('span')
                    if date_element:
                        post_date = await date_element.inner_text()
                    else:
                        post_date = "hace 1 semana"  # Default
                    
                    # Filtrar por antigüedad
                    if self.is_within_max_weeks(post_date):
                        posts.append({
                            'text': post_text,
                            'date': post_date,
                            'extracted_at': datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    print(f"Error al extraer post individual: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error general al extraer posts: {e}")
            
        return posts
    
    async def run_scraping_cycle(self):
        """Ejecutar ciclo completo de scraping"""
        try:
            await self.init_browser()
            
            # FASE 1: Demanda
            for term in self.config.DEMANDA_TERMS:
                posts = await self.search_facebook(term, "DEMANDA")
                await self.random_pause()  # Pausa larga entre búsquedas
            
            # FASE 2: Oferta  
            for term in self.config.OFERTA_TERMS:
                posts = await self.search_facebook(term, "OFERTA")
                await self.random_pause()  # Pausa larga entre búsquedas
            
            # Guardar estado
            await self.save_state()
            
            return True
            
        except Exception as e:
            print(f"✗ Error en ciclo de scraping: {e}")
            return False
            
        finally:
            # Cerrar navegador para liberar memoria
            if self.browser:
                await self.browser.close()
                print("✓ Navegador cerrado - memoria liberada")
    
    async def __aenter__(self):
        await self.init_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
