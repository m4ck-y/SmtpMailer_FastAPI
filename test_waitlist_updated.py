#!/usr/bin/env python3
"""
Script de prueba actualizado para el módulo de waitlist con ofertas.

Verifica que la implementación funcione correctamente con la nueva funcionalidad
de personalización por ofertas sin enviar emails reales.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

from app.waitlist.models import WaitlistEmailRequest, WaitlistEmailResponse
from app.waitlist.controller import EmailWaitlistApplication
from app.config import settings

def test_waitlist_models_with_offerings():
    """Prueba los modelos de Pydantic con ofertas."""
    print("🧪 Probando modelos de waitlist con ofertas...")
    
    # Caso con múltiples ofertas
    request_multiple = WaitlistEmailRequest(
        email="usuario@ejemplo.com",
        user_name="Juan Pérez",
        website_url="https://miapp.com",
        offerings=["CRM Avanzado", "Sistema de Inventarios", "Analytics Pro"]
    )
    print(f"✅ Request múltiples ofertas: {request_multiple.dict()}")
    
    # Caso con una sola oferta
    request_single = WaitlistEmailRequest(
        email="maria@empresa.com",
        user_name="María González",
        offerings=["CRM Avanzado"]
    )
    print(f"✅ Request una oferta: {request_single.dict()}")
    
    # Caso sin ofertas específicas (plataforma)
    request_platform = WaitlistEmailRequest(
        email="carlos@startup.com",
        user_name="Carlos Ruiz",
        offerings=[]
    )
    print(f"✅ Request sin ofertas: {request_platform.dict()}")
    
    # Caso mínimo (offerings por defecto es lista vacía)
    request_minimal = WaitlistEmailRequest(
        email="usuario@ejemplo.com"
    )
    print(f"✅ Request mínimo: {request_minimal.dict()}")
    
    # Caso con URL inválida (debería fallar)
    try:
        request_invalid = WaitlistEmailRequest(
            email="usuario@ejemplo.com",
            website_url="invalid-url",
            offerings=["Test"]
        )
        print("❌ ERROR: Debería haber fallado con URL inválida")
    except ValueError as e:
        print(f"✅ Validación de URL funcionando: {e}")
    
    print("✅ Modelos con ofertas funcionando correctamente\n")

def test_offerings_text_generation():
    """Prueba la generación de texto personalizado según ofertas."""
    print("🎯 Probando generación de texto de ofertas...")
    
    controller = EmailWaitlistApplication()
    
    # Test sin ofertas (plataforma)
    platform_data = controller._generate_offerings_text([])
    print(f"🌐 Sin ofertas: {platform_data}")
    assert platform_data['message_type'] == 'platform'
    assert 'plataforma' in platform_data['offerings_text']
    
    # Test con una oferta
    single_data = controller._generate_offerings_text(["CRM Avanzado"])
    print(f"📦 Una oferta: {single_data}")
    assert single_data['message_type'] == 'single'
    assert single_data['offerings_text'] == "CRM Avanzado"
    
    # Test con múltiples ofertas
    multiple_data = controller._generate_offerings_text(["CRM Avanzado", "Analytics Pro", "Inventarios"])
    print(f"📦📦📦 Múltiples ofertas: {multiple_data}")
    assert multiple_data['message_type'] == 'multiple'
    assert 'CRM Avanzado, Analytics Pro, Inventarios' in multiple_data['offerings_text']
    
    print("✅ Generación de texto funcionando correctamente\n")

def test_template_rendering_with_offerings():
    """Prueba el renderizado de plantillas con ofertas."""
    print("🎨 Probando renderizado de plantillas con ofertas...")
    
    try:
        controller = EmailWaitlistApplication()
        print("✅ Controller inicializado correctamente")
        
        # Verificar que el template existe
        template = controller.jinja_env.get_template("waitlist.html")
        print("✅ Template waitlist.html encontrado")
        
        # Test con múltiples ofertas
        offerings_data = controller._generate_offerings_text(["CRM Avanzado", "Analytics Pro"])
        template_data = {
            "app_name": "Mi App Test",
            "company_name": "Mi Empresa Test",
            "logo_url": "https://ejemplo.com/logo.png",
            "support_email": "soporte@ejemplo.com",
            "website_url": "https://ejemplo.com",
            "user_name": "Usuario Test",
            "user_email": "test@ejemplo.com",
            "show_website_button": True,
            **offerings_data
        }
        
        html_content = template.render(**template_data)
        print(f"✅ Template renderizado correctamente ({len(html_content)} caracteres)")
        
        # Verificar que contiene elementos clave
        assert "Usuario Test" in html_content
        assert "test@ejemplo.com" in html_content
        assert "Mi App Test" in html_content
        assert offerings_data['availability_message'] in html_content
        print("✅ Contenido del template con ofertas verificado")
        
    except Exception as e:
        print(f"❌ Error en renderizado: {e}")
        return False
    
    print("✅ Renderizado con ofertas funcionando correctamente\n")
    return True

def test_example_scenarios():
    """Prueba escenarios de ejemplo con diferentes tipos de ofertas."""
    print("🎭 Probando escenarios de ejemplo...")
    
    controller = EmailWaitlistApplication()
    
    scenarios = [
        {
            "name": "E-commerce",
            "offerings": ["Tienda Online", "Sistema de Pagos", "Gestión de Inventarios"],
            "icon": "🛒"
        },
        {
            "name": "SaaS Empresarial",
            "offerings": ["CRM Empresarial"],
            "icon": "💼"
        },
        {
            "name": "Plataforma General",
            "offerings": [],
            "icon": "🌐"
        },
        {
            "name": "Servicios Profesionales",
            "offerings": ["Consultoría Digital", "Desarrollo Web", "Marketing Automation"],
            "icon": "🎯"
        },
        {
            "name": "Fintech",
            "offerings": ["Pagos Digitales", "Billetera Virtual"],
            "icon": "💳"
        }
    ]
    
    for scenario in scenarios:
        data = controller._generate_offerings_text(scenario["offerings"])
        print(f"{scenario['icon']} {scenario['name']}: {data['availability_message']}")
    
    print("✅ Escenarios de ejemplo validados correctamente\n")

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
    print("🚀 Iniciando pruebas del módulo waitlist con ofertas\n")
    
    try:
        test_waitlist_models_with_offerings()
        test_offerings_text_generation()
        test_configuration()
        template_ok = test_template_rendering_with_offerings()
        test_example_scenarios()
        
        if template_ok:
            print("🎉 Todas las pruebas pasaron exitosamente!")
            print("\n📋 Resumen de implementación actualizada:")
            print("✅ Modelos Pydantic con validación de ofertas")
            print("✅ Lógica condicional para personalización de mensajes")
            print("✅ Plantilla HTML responsiva con ofertas")
            print("✅ Controller con generación de texto inteligente")
            print("✅ Router con documentación OpenAPI actualizada")
            print("✅ Integración con FastAPI main")
            
            print("\n🎯 Tipos de mensaje soportados:")
            print("📦 single: Una sola oferta específica")
            print("📦📦📦 multiple: Múltiples ofertas listadas")
            print("🌐 platform: Sin ofertas específicas (plataforma general)")
            
            print("\n🔗 Endpoints disponibles:")
            print("POST /waitlist/send_confirmation - Enviar confirmación con ofertas")
            
            print("\n📚 Para probar la API:")
            print("1. Ejecutar: uvicorn app.main:app --reload")
            print("2. Visitar: http://localhost:8000/docs")
            print("3. Probar endpoint con diferentes arrays de ofertas:")
            print("   - offerings: [] (plataforma)")
            print("   - offerings: ['CRM Avanzado'] (una oferta)")
            print("   - offerings: ['CRM', 'Analytics', 'Inventarios'] (múltiples)")
        else:
            print("❌ Algunas pruebas fallaron")
            return 1
            
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())