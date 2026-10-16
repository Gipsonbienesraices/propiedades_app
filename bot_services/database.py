"""
Gestor de Base de Datos PostgreSQL en la Nube
Soporta Supabase y Neon para almacenamiento de leads
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
from .config import BotConfig

class DatabaseManager:
    def __init__(self):
        self.config = BotConfig()
        self.database_url = self.config.DATABASE_URL
        
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def init_tables(self):
        """Inicializar tablas para leads"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Tabla de Demanda
            cur.execute('''
                CREATE TABLE IF NOT EXISTS demanda (
                    id SERIAL PRIMARY KEY,
                    post_text TEXT NOT NULL,
                    post_date TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    category TEXT NOT NULL,
                    subcategory TEXT,
                    sector TEXT,
                    price_budget REAL,
                    phones TEXT[],
                    name TEXT,
                    processed BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Tabla de Oferta
            cur.execute('''
                CREATE TABLE IF NOT EXISTS oferta (
                    id SERIAL PRIMARY KEY,
                    post_text TEXT NOT NULL,
                    post_date TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    category TEXT NOT NULL,
                    subcategory TEXT,
                    sector TEXT,
                    price_budget REAL,
                    phones TEXT[],
                    name TEXT,
                    processed BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Tabla de Matches
            cur.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id SERIAL PRIMARY KEY,
                    demand_id INTEGER REFERENCES demanda(id),
                    offer_id INTEGER REFERENCES oferta(id),
                    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    match_type TEXT,
                    alert_sent BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Tabla de Comentarios
            cur.execute('''
                CREATE TABLE IF NOT EXISTS comentarios (
                    id SERIAL PRIMARY KEY,
                    lead_id INTEGER,
                    lead_category TEXT,
                    comment_text TEXT NOT NULL,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    lead_post_date DATE
                )
            ''')
            
            conn.commit()
            cur.close()
            conn.close()
            
            print("✓ Tablas de base de datos inicializadas")
            return True
            
        except Exception as e:
            print(f"✗ Error al inicializar tablas: {e}")
            return False
    
    async def save_lead(self, lead_data, table='demanda'):
        """Guardar lead en base de datos"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Determinar tabla según clasificación
            if lead_data['classification']['category'] == 'Comprador':
                table = 'demanda'
            elif lead_data['classification']['category'] == 'Vendedor':
                table = 'oferta'
            else:
                cur.close()
                conn.close()
                return False
            
            cur.execute(f'''
                INSERT INTO {table} 
                (post_text, post_date, extracted_at, category, subcategory, sector, price_budget, phones, name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                lead_data['post_text'],
                lead_data['post_date'],
                lead_data['extracted_at'],
                lead_data['classification']['category'],
                lead_data['classification']['subcategory'],
                lead_data['sector'],
                lead_data['price_budget'],
                lead_data['phones'],
                lead_data['name']
            ))
            
            lead_id = cur.fetchone()['id']
            conn.commit()
            cur.close()
            conn.close()
            
            return lead_id
            
        except Exception as e:
            print(f"✗ Error al guardar lead: {e}")
            return False
    
    async def get_leads_by_category(self, categories):
        """Obtener leads por categoría"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            leads = []
            for category in categories:
                # Buscar en ambas tablas
                for table in ['demanda', 'oferta']:
                    cur.execute(f'''
                        SELECT * FROM {table} 
                        WHERE subcategory = %s 
                        AND processed = FALSE
                        ORDER BY extracted_at DESC
                    ''', (category,))
                    
                    leads.extend(cur.fetchall())
            
            cur.close()
            conn.close()
            
            return leads
            
        except Exception as e:
            print(f"✗ Error al obtener leads: {e}")
            return []
    
    async def match_alert_exists(self, match):
        """Verificar si ya existe alerta para este match"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute('''
                SELECT id FROM matches 
                WHERE demand_id = %s AND offer_id = %s
            ''', (match['demand_lead'].get('id'), match['offer_lead'].get('id')))
            
            exists = cur.fetchone() is not None
            cur.close()
            conn.close()
            
            return exists
            
        except Exception as e:
            print(f"✗ Error al verificar match: {e}")
            return False
    
    async def save_match_alert(self, match):
        """Guardar registro de alerta enviada"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute('''
                INSERT INTO matches (demand_id, offer_id, match_type, alert_sent)
                VALUES (%s, %s, %s, %s)
            ''', (
                match['demand_lead'].get('id'),
                match['offer_lead'].get('id'),
                match['match_type'],
                True
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"✗ Error al guardar match: {e}")
            return False
    
    async def get_daily_comment_count(self, comment_date):
        """Obtener conteo de comentarios del día"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute('''
                SELECT COUNT(*) as count FROM comentarios 
                WHERE lead_post_date = %s
            ''', (comment_date,))
            
            count = cur.fetchone()['count']
            cur.close()
            conn.close()
            
            return count
            
        except Exception as e:
            print(f"✗ Error al obtener conteo diario: {e}")
            return 0
    
    async def get_last_comment_time(self):
        """Obtener hora del último comentario"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute('''
                SELECT posted_at FROM comentarios 
                ORDER BY posted_at DESC 
                LIMIT 1
            ''')
            
            result = cur.fetchone()
            cur.close()
            conn.close()
            
            if result:
                return result['posted_at']
            return None
            
        except Exception as e:
            print(f"✗ Error al obtener último comentario: {e}")
            return None
    
    async def save_comment_record(self, lead, comment_text):
        """Guardar registro de comentario"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Extraer fecha del post
            post_date = datetime.now().date()
            
            cur.execute('''
                INSERT INTO comentarios (lead_id, lead_category, comment_text, lead_post_date)
                VALUES (%s, %s, %s, %s)
            ''', (
                lead.get('id'),
                lead['classification']['subcategory'],
                comment_text,
                post_date
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"✗ Error al guardar comentario: {e}")
            return False
