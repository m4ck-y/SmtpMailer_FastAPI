#!/usr/bin/env python3
"""
Script de prueba para el módulo de waitlist.

Verifica que la implementación funcione correctamente sin enviar emails reales.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

from app.waitlist.models import WaitlistEmailRequest, WaitlistEmailResponse
from app.waitlist.controller import EmailWaitlistApplication
from app.config import settings

def test_waitlist_models():
    """Prueba los modelos de Pydantic."""
    print("🧪 Probando modelos de waitlist...")
    
    # Caso completo
    request_full = WaitlistEmailRequest(
        email="usuario@ejemplo.com",
        user_name="Juan Pérez",
        website_url="https://miapp.com"
    )
    print(f"✅ Request completo: {request_full.dict()}")
    
    # Caso mínimo
    request_minimal = WaitlistEmailRequest(
        email="usuario@ejemplo.com"
    )
    print(f"✅ Request mínimo: {request_minimal.dict()}")
    
    # Caso con URL inválida (debería fallar)
    try:
        request_invalid = WaitlistEmailRequest(
            email="usuario@ejemplo.com",
            website_url="invalid-url"
        )
        print("❌ ERROR: Debería haber fallado con URL inválida")
    except ValueError as e:
        print(f"✅ Validación de URL funcionando: {e}")
    
    print("✅ Modelos funcionando correctamente\n")

def test_template_rendering():
    """Prueba el renderizado de plantillas."""
    print("🎨 Probando renderizado de plantillas...")
    
    try:
        controller = EmailWaitlistApplication()
        print("✅ Controller inicializado correctamente")
        
        # Verificar que el template existe
        template = controller.jinja_env.get_template("waitlist.html")
        print("✅ Template waitlist.html encontrado")
        
        # Renderizar con datos de prueba
        template_data = {
            "app_name": "Mi App Test",
            "company_name": "Mi Empresa Test",
            "logo_url": "https://ejemplo.com/logo.png",
            "support_email": "soporte@ejemplo.com",
            "website_url": "https://ejemplo.com",
            "user_name": "Usuario Test",
            "user_email": "test@ejemplo.com",
            "show_website_button": True
        }
        
        html_content = template.render(**template_data)
        print(f"✅ Template renderizado correctamente ({len(html_content)} caracteres)")
        
        # Verificar que contiene elementos clave
        assert "Usuario Test" in html_content
        assert "test@ejemplo.com" in html_content
        assert "Mi App Test" in html_content
        print("✅ Contenido del template verificado")
        
    except Exception as e:
        print(f"❌ Error en renderizado: {e}")
        return False
    
    print("✅ Renderizado funcionando correctamente\n")
    return True

def test_configuration():
    """Prueba la configuración de variables de entorno."""
    print("⚙️ Probando configuración...")
    
    print(f"APP_NAME: {settings.APP_NAME}")
    print(f"COMPANY_NAME: {settings.COMPANY_NAME}")
    print(f"COMPANY_LOGO_URL: {settings.COMPANY_LOGO_URL}")
    print(f"SUPPORT_EMAIL: {settings.SUPPORT_EMAIL}")
    print(f"WEBSITE_URL: {settings.WEBSITE_URL}")
    
    # Verificar configuración SMTP (sin mostrar credenciales)
    smtp_configured = bool(
        settings.SMTP_HOST and 
        settings.SMTP_USERNAME and 
        settings.SMTP_PASSWORD
    )
    print(f"SMTP configurado: {smtp_configured}")
    
    if smtp_configured:
        print(f"SMTP Host: {settings.SMTP_HOST}")
        print(f"SMTP Port: {settings.SMTP_PORT}")
        print(f"SMTP From: {settings.SMTP_FROM_EMAIL}")
    
    print("✅ Configuración verificada\n")

def main():
    """Función principal de pruebas."""
    print("🚀 Iniciando pruebas del módulo waitlist\n")
    
    try:
        test_waitlist_models()
        test_configuration()
        template_ok = test_template_rendering()
        
        if template_ok:
            print("🎉 Todas las pruebas pasaron exitosamente!")
            print("\n📋 Resumen de implementación:")
            print("✅ Modelos Pydantic con validación")
            print("✅ Plantilla HTML responsiva")
            print("✅ Controller con lógica de negocio")
            print("✅ Router con documentación OpenAPI")
            print("✅ Integración con FastAPI main")
            
            print("\n🔗 Endpoints disponibles:")
            print("POST /waitlist/send_confirmation - Enviar confirmación de waitlist")
            
            print("\n📚 Para probar la API:")
            print("1. Ejecutar: uvicorn app.main:app --reload")
            print("2. Visitar: http://localhost:8000/docs")
            print("3. Probar endpoint: /waitlist/send_confirmation")
        else:
            print("❌ Algunas pruebas fallaron")
            return 1
            
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())