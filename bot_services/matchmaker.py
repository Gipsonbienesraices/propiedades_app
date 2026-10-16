"""
Motor de Emparejamiento y Alertas por Telegram
Cruza tablas de Demanda y Oferta para encontrar coincidencias
"""

import asyncio
import aiohttp
from datetime import datetime
from .config import BotConfig

class Matchmaker:
    def __init__(self, database_manager):
        self.db = database_manager
        self.config = BotConfig()
        self.telegram_token = self.config.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = self.config.TELEGRAM_CHAT_ID
        
    async def find_matches(self):
        """Buscar coincidencias entre demanda y oferta"""
        try:
            # Obtener leads de demanda
            demand_leads = await self.db.get_leads_by_category(['Busca Arriendo', 'Busca Compra'])
            
            # Obtener leads de oferta
            offer_leads = await self.db.get_leads_by_category(['Ofrece Arriendo', 'Ofrece Venta'])
            
            matches = []
            
            for demand in demand_leads:
                for offer in offer_leads:
                    # Verificar coincidencia por sector
                    if self.sector_match(demand.get('sector', ''), offer.get('sector', '')):
                        # Verificar coincidencia por presupuesto/precio
                        if self.price_match(demand.get('price_budget'), offer.get('price_budget')):
                            # Verificar subcategoría compatible
                            demand_subcat = demand.get('subcategory', '')
                            offer_subcat = offer.get('subcategory', '')
                            if self.subcategory_match(demand_subcat, offer_subcat):
                                match = {
                                    'demand_lead': demand,
                                    'offer_lead': offer,
                                    'match_date': datetime.now().isoformat(),
                                    'match_type': self.determine_match_type(demand, offer)
                                }
                                matches.append(match)
            
            print(f"✓ Encontrados {len(matches)} matches")
            return matches
            
        except Exception as e:
            print(f"✗ Error al buscar matches: {e}")
            return []
    
    def sector_match(self, sector1, sector2):
        """Verificar coincidencia de sector"""
        # Coincidencia exacta
        if sector1 == sector2:
            return True
        
        # Coincidencia parcial (mismo área geográfica)
        if sector1 != "No especificado" and sector2 != "No especificado":
            return True
        
        return False
    
    def price_match(self, demand_budget, offer_price):
        """Verificar coincidencia de presupuesto/precio"""
        if not demand_budget or not offer_price:
            return True  # Si no hay información, considerar match
        
        # Tolerancia del 20%
        lower_bound = demand_budget * 0.8
        upper_bound = demand_budget * 1.2
        
        return lower_bound <= offer_price <= upper_bound
    
    def subcategory_match(self, demand_subcat, offer_subcat):
        """Verificar compatibilidad de subcategorías"""
        # Compatible: Busca Arriendo + Ofrece Arriendo
        if demand_subcat == "Busca Arriendo" and offer_subcat == "Ofrece Arriendo":
            return True
        
        # Compatible: Busca Compra + Ofrece Venta
        if demand_subcat == "Busca Compra" and offer_subcat == "Ofrece Venta":
            return True
        
        return False
    
    def determine_match_type(self, demand, offer):
        """Determinar tipo de match"""
        demand_type = demand['classification']['subcategory']
        offer_type = offer['classification']['subcategory']
        
        if "Arriendo" in demand_type and "Arriendo" in offer_type:
            return "Match Arriendo"
        elif "Compra" in demand_type and "Venta" in offer_type:
            return "Match Compra-Venta"
        else:
            return "Mixto"
    
    async def send_telegram_alert(self, match):
        """Enviar alerta de match por Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            print("⚠️ Token o Chat ID de Telegram no configurados")
            return False
        
        try:
            demand = match['demand_lead']
            offer = match['offer_lead']
            
            # Formatear mensaje
            message = f"""
🔥 MATCH ENCONTRADO: {match['match_type']}

📍 Sector: {demand['sector']}

👤 El que busca:
   Tipo: {demand['classification']['subcategory']}
   Teléfono: {demand['phones'][0] if demand['phones'] else 'No disponible'}
   Presupuesto: ${demand['price_budget'] if demand['price_budget'] else 'No especificado'}

🏠 El que ofrece:
   Tipo: {offer['classification']['subcategory']}
   Teléfono: {offer['phones'][0] if offer['phones'] else 'No disponible'}
   Precio: ${offer['price_budget'] if offer['price_budget'] else 'No especificado'}

📅 Fecha del match: {match['match_date']}
"""
            
            # Enviar a Telegram
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        print(f"✓ Alerta enviada: {match['match_type']} en {demand['sector']}")
                        return True
                    else:
                        print(f"✗ Error al enviar alerta: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"✗ Error al enviar alerta Telegram: {e}")
            return False
    
    async def process_matches(self):
        """Procesar todos los matches y enviar alertas"""
        matches = await self.find_matches()
        
        for match in matches:
            # Verificar si ya se envió alerta para este match
            if not await self.db.match_alert_exists(match):
                await self.send_telegram_alert(match)
                # Guardar que se envió la alerta
                await self.db.save_match_alert(match)
        
        return len(matches)
    
    async def run_matchmaking_cycle(self):
        """Ejecutar ciclo completo de matchmaking"""
        try:
            print("🔄 Iniciando ciclo de matchmaking...")
            matches_found = await self.process_matches()
            print(f"✓ Ciclo de matchmaking completado: {matches_found} matches procesados")
            return True
        except Exception as e:
            print(f"✗ Error en ciclo de matchmaking: {e}")
            return False
