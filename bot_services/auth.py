"""
Script de Autenticación de Facebook
Permite login manual y guarda la sesión en state.json
"""

import asyncio
import json
import os
from playwright.async_api import async_playwright

async def authenticate_facebook():
    """Autenticar en Facebook manualmente"""
    print("Iniciando autenticacion de Facebook...")
    print("Abre la ventana que aparecera e inicia sesion manualmente")
    
    playwright = await async_playwright().start()
    
    # Navegador en modo visible para login manual
    browser = await playwright.chromium.launch(headless=False)
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    page = await context.new_page()
    
    try:
        # Navegar a Facebook
        await page.goto('https://www.facebook.com')
        print("Navegando a Facebook...")
        
        # Esperar a que el usuario inicie sesión manualmente
        print("Por favor inicia sesion en la ventana abierta...")
        print("   El script esperara hasta que detectes que estas logueado")
        
        # Esperar a que el usuario esté logueado (verificar cambio de URL)
        await page.wait_for_url('https://www.facebook.com/*', timeout=300000)  # 5 minutos
        
        # Esperar adicional para asegurar login completo
        await asyncio.sleep(5)
        
        # Guardar estado (cookies, etc.)
        state = {
            'cookies': await context.cookies(),
            'storage_state': await context.storage_state()
        }
        
        # Usar ruta absoluta
        state_file = os.path.join(os.path.dirname(__file__), 'state.json')
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"Sesion guardada en {state_file}")
        print("Autenticacion completada exitosamente")
        
        # Mantener navegador abierto un momento para verificar
        print("Navegador permanecera abierto 10 segundos para verificacion...")
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"Error durante autenticacion: {e}")
        
    finally:
        await browser.close()
        await playwright.stop()
        print("Navegador cerrado")

if __name__ == '__main__':
    asyncio.run(authenticate_facebook())
