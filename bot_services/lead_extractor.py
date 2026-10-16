"""
Extractor y Clasificador de Leads
Procesa posts de Facebook y clasifica por categoría
"""

import re
import os
from datetime import datetime
from .config import BotConfig

class LeadExtractor:
    def __init__(self):
        self.config = BotConfig()
        
    def classify_lead(self, post_text):
        """Clasificar lead según su contenido"""
        post_lower = post_text.lower()
        
        classification = {
            'category': None,
            'subcategory': None,
            'confidence': 0.0
        }
        
        # Clasificación de Comprador
        if any(keyword in post_lower for keyword in self.config.BUYER_KEYWORDS):
            classification['category'] = 'Comprador'
            classification['confidence'] = 0.8
            
            # Subclasificación
            if any(keyword in post_lower for keyword in self.config.RENT_SEEKER_KEYWORDS):
                classification['subcategory'] = 'Busca Arriendo'
                classification['confidence'] = 0.9
            else:
                classification['subcategory'] = 'Busca Compra'
        
        # Clasificación de Vendedor
        elif any(keyword in post_lower for keyword in self.config.SELLER_KEYWORDS):
            classification['category'] = 'Vendedor'
            classification['confidence'] = 0.8
            
            # Subclasificación
            if any(keyword in post_lower for keyword in self.config.RENT_OFFERER_KEYWORDS):
                classification['subcategory'] = 'Ofrece Arriendo'
                classification['confidence'] = 0.9
            else:
                classification['subcategory'] = 'Ofrece Venta'
        
        return classification
    
    def extract_sector(self, post_text):
        """Extraer sector/mención geográfica"""
        # Lista de sectores comunes en Ecuador
        sectores = [
            'carolina', 'cumbayá', 'tumbaco', 'quito', 'sur', 'norte', 
            'centro', 'valles', 'la florida', 'el condado', 'san rafael',
            'la villaflora', 'chalde', 'solanda', 'la ferroviaria',
            'la argelia', 'la Kennedy', 'la comuna', 'san borja',
            'independencia', 'cotocollao', 'el batán', 'puengasí',
            'pichincha', 'cayambe', 'mejía', 'rumiñahui'
        ]
        
        post_lower = post_text.lower()
        found_sectores = [sector for sector in sectores if sector in post_lower]
        
        return found_sectores[0] if found_sectores else "No especificado"
    
    def extract_price_budget(self, post_text):
        """Extraer precio o presupuesto usando expresiones regulares"""
        # Patrones para precios: $100, $1000, $1,000, etc.
        price_patterns = [
            r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,000.00
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s* dólares',  # 1000 dólares
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*usd',  # 1000 usd
            r'presupuesto\s*[:]\s*(\d+)',  # presupuesto: 1000
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, post_text, re.IGNORECASE)
            if matches:
                # Limpiar y convertir a número
                price_str = matches[0].replace(',', '').replace('$', '').strip()
                try:
                    return float(price_str)
                except ValueError:
                    continue
        
        return None
    
    def extract_phones(self, post_text):
        """Extraer números de teléfono ecuatorianos (10 dígitos)"""
        # Patrones para teléfonos ecuatorianos
        phone_patterns = [
            r'09\d{8}',  # 09xxxxxxxx
            r'\+593\s*9\d{8}',  # +593 9xxxxxxxx
            r'593\s*9\d{8}',  # 593 9xxxxxxxx
            r'0\d{9}',  # 0xxxxxxxxx
        ]
        
        phones = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, post_text)
            for match in matches:
                # Normalizar a formato 10 dígitos
                phone = re.sub(r'[^\d]', '', match)
                if len(phone) == 10 and phone.startswith('0'):
                    phones.append(phone)
                elif len(phone) == 10 and phone.startswith('9'):
                    phones.append('0' + phone)
                elif len(phone) == 11 and phone.startswith('593'):
                    phones.append('0' + phone[3:])
        
        return list(set(phones))  # Eliminar duplicados
    
    def extract_name(self, post_text):
        """Extraer nombre del autor (simplificado)"""
        # En producción esto sería más complejo
        # Por ahora retorna "No identificado"
        return "No identificado"
    
    def process_post(self, post_data):
        """Procesar un post completo y extraer toda la información"""
        post_text = post_data.get('text', '')
        
        lead_data = {
            'post_text': post_text,
            'post_date': post_data.get('date', ''),
            'extracted_at': post_data.get('extracted_at', datetime.now().isoformat()),
            'classification': self.classify_lead(post_text),
            'sector': self.extract_sector(post_text),
            'price_budget': self.extract_price_budget(post_text),
            'phones': self.extract_phones(post_text),
            'name': self.extract_name(post_text)
        }
        
        return lead_data
    
    def filter_leads(self, leads):
        """Filtrar leads según criterios de calidad"""
        filtered_leads = []
        
        for lead in leads:
            # Solo leads con clasificación exitosa
            if lead['classification']['category']:
                # Solo leads con teléfono (opcional)
                if lead['phones']:
                    filtered_leads.append(lead)
        
        return filtered_leads
