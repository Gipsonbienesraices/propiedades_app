"""
Auto-Comentador con Límites Anti-Ban
Comenta solo en leads relevantes con control estricto de frecuencia
"""

import random
import asyncio
import os
from datetime import datetime, timedelta
from .config import BotConfig

class AutoCommenter:
    def __init__(self, database_manager):
        self.db = database_manager
        self.config = BotConfig()
        self.my_phone = os.getenv('MY_PHONE_NUMBER', '0987654321')  # Tu número
        
    def is_eligible_for_comment(self, lead):
        """Verificar si el lead es elegible para recibir comentario"""
        classification = lead['classification']
        
        # Solo comentar en Comprador o Busca Arriendo
        if classification['category'] == 'Comprador':
            return True
        if classification['subcategory'] == 'Busca Arriendo':
            return True
            
        return False
    
    def generate_comment(self, lead):
        """Generar comentario usando Spintax"""
        messages = self.config.COMMENT_MESSAGES
        selected_message = random.choice(messages)
        
        # Reemplazar variables
        nombre = lead['name'] if lead['name'] != "No identificado" else "amigo"
        
        # Determinar tipo de búsqueda
        if lead['classification']['subcategory'] == 'Busca Arriendo':
            tipo_buscado = "arriendo"
        elif lead['classification']['subcategory'] == 'Busca Compra':
            tipo_buscado = "compra"
        else:
            tipo_buscado = "propiedad"
        
        comment = selected_message.format(
            nombre=nombre,
            tipo=tipo_buscado,
            telefono=self.my_phone
        )
        
        return comment
    
    async def can_comment_now(self):
        """Verificar si se puede comentar ahora según límites"""
        now = datetime.now()
        
        # Verificar límite diario
        daily_count = await self.db.get_daily_comment_count(now.date())
        if daily_count >= self.config.MAX_DAILY_COMMENTS:
            print(f"⚠️ Límite diario alcanzado: {daily_count}/{self.config.MAX_DAILY_COMMENTS}")
            return False
        
        # Verificar intervalo mínimo
        last_comment_time = await self.db.get_last_comment_time()
        if last_comment_time:
            time_since_last = now - last_comment_time
            min_interval = timedelta(minutes=self.config.COMMENT_INTERVAL_MINUTES)
            
            if time_since_last < min_interval:
                wait_minutes = (min_interval - time_since_last).total_seconds() / 60
                print(f"⏸️ Esperar {wait_minutes:.1f} minutos antes de próximo comentario")
                return False
        
        return True
    
    async def post_comment(self, lead, page):
        """Publicar comentario en Facebook"""
        try:
            comment_text = self.generate_comment(lead)
            
            # En producción esto encontraría el elemento de comentario
            # y simularía la acción de comentar
            # Por ahora es una simulación
            
            print(f"💬 Comentario generado para {lead['name']}:")
            print(f"   {comment_text}")
            
            # Simular acción de comentar
            await asyncio.sleep(random.uniform(2, 4))  # Simular tiempo de escribir
            
            # Guardar registro del comentario
            await self.db.save_comment_record(lead, comment_text)
            
            return True
            
        except Exception as e:
            print(f"✗ Error al comentar: {e}")
            return False
    
    async def process_comment_cycle(self, leads, page):
        """Procesar ciclo de comentarios"""
        if not await self.can_comment_now():
            print("⏸️ No se puede comentar ahora por límites")
            return 0
        
        # Filtrar leads elegibles
        eligible_leads = [lead for lead in leads if self.is_eligible_for_comment(lead)]
        
        if not eligible_leads:
            print("📭 No hay leads elegibles para comentar")
            return 0
        
        # Seleccionar lead aleatorio
        selected_lead = random.choice(eligible_leads)
        
        # Publicar comentario
        success = await self.post_comment(selected_lead, page)
        
        if success:
            print(f"✓ Comentario publicado para {selected_lead['name']}")
            return 1
        else:
            print(f"✗ Falló publicación de comentario")
            return 0
    
    async def run_commenting_cycle(self, leads, page):
        """Ejecutar ciclo completo de comentarios"""
        try:
            print("💬 Iniciando ciclo de comentarios...")
            comments_posted = await self.process_comment_cycle(leads, page)
            print(f"✓ Ciclo de comentarios completado: {comments_posted} comentarios")
            return comments_posted
        except Exception as e:
            print(f"✗ Error en ciclo de comentarios: {e}")
            return 0
