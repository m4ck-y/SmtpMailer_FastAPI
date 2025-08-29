from fastapi import APIRouter, HTTPException, status
from app.waitlist.controller import EmailWaitlistApplication
from app.waitlist.models import WaitlistEmailRequest, WaitlistEmailResponse

controller = EmailWaitlistApplication()

MODULE_NAME = "waitlist"

router_waitlist = APIRouter(
    prefix=f"/{MODULE_NAME}",
    tags=[MODULE_NAME])

TAG_WAITLIST = {
    "name": MODULE_NAME,
    "description": """
📧 **Confirmación de Lista de Espera** - Notificaciones personalizadas por ofertas

### 🎯 Funcionalidades Principales:
- **Confirmación automática** - Email inmediato tras registro en waitlist
- **Personalización inteligente** - Mensaje adaptado según ofertas de interés
- **Diseño responsivo** - Compatible con todos los clientes de correo
- **Lógica condicional** - Diferentes mensajes según cantidad de ofertas

### 📋 Personalización por Ofertas:
- **Sin ofertas específicas** - Mensaje genérico de plataforma
- **Una oferta** - "En cuanto [Oferta] esté disponible oficialmente..."
- **Múltiples ofertas** - "En cuanto nuestras soluciones [Lista] estén disponibles..."
- **Validación automática** - Máximo 10 ofertas, 100 caracteres cada una

### 🚀 Casos de Uso por Escenario:
- **Plataforma general:** `offerings: []` - Registro sin ofertas específicas
- **Producto único:** `offerings: ["CRM Avanzado"]` - Una solución particular
- **Suite completa:** `offerings: ["CRM", "Analytics", "Inventarios"]` - Múltiples productos
- **Beta testing:** `offerings: ["Beta Program"]` - Programas de prueba

### ⚡ Integración Avanzada:
- **Array de ofertas** - Parámetro principal para personalización
- **Respuesta detallada** - Incluye tipo de mensaje y texto generado
- **Configuración automática** - Branding desde variables de entorno
- **Manejo robusto** - Validación y errores SMTP cubiertos

### 🔧 Tipos de Respuesta:
- **message_type: "platform"** - Sin ofertas específicas
- **message_type: "single"** - Una sola oferta
- **message_type: "multiple"** - Múltiples ofertas
- **offerings_text** - Texto exacto generado para el email
"""
}

@router_waitlist.post("/send_confirmation", response_model=WaitlistEmailResponse)
def enviar_confirmacion_waitlist(request: WaitlistEmailRequest) -> WaitlistEmailResponse:
    """
    Envía email de confirmación de registro en lista de espera con personalización de ofertas.
    
    Notifica al usuario que su correo electrónico ha sido registrado exitosamente
    en la lista de espera. El mensaje se personaliza automáticamente según las
    ofertas (productos/servicios) especificadas, utilizando lógica condicional
    inteligente para diferentes escenarios.
    
    ### 🎯 Personalización Inteligente por Ofertas:
    - **Sin ofertas (array vacío):** "En cuanto nuestra plataforma esté disponible..."
    - **Una oferta:** "En cuanto [Nombre de la Oferta] esté disponible oficialmente..."
    - **Múltiples ofertas:** "En cuanto nuestras soluciones [Oferta1, Oferta2, Oferta3] estén disponibles..."
    
    ### 📧 Características del Email:
    - **Confirmación inmediata:** Notificación instantánea de registro exitoso
    - **Mensaje contextual:** Personalizado según ofertas de interés del usuario
    - **Branding consistente:** Logo y colores corporativos automáticos
    - **Diseño responsivo:** Compatible con todos los clientes de correo
    
    ### 🎨 Personalización Automática:
    - **Nombre del usuario:** Personalización del saludo (opcional)
    - **Logo corporativo:** Configurado automáticamente desde variables de entorno
    - **Botón de acción:** Enlace opcional al sitio web principal
    - **Información de contacto:** Email de soporte para consultas
    - **Mensaje de disponibilidad:** Generado según ofertas especificadas
    
    ### ⚡ Casos de Uso por Tipo de Ofertas:
    - **Plataforma general:** `offerings: []` - Para registro general sin ofertas específicas
    - **Producto específico:** `offerings: ["CRM Avanzado"]` - Para una solución particular
    - **Suite de productos:** `offerings: ["CRM", "Analytics", "Inventarios"]` - Para múltiples soluciones
    - **Beta testing:** `offerings: ["Beta Program"]` - Para programas de prueba
    
    ### 🔧 Configuración Automática:
    - `app_name`: Nombre de la aplicación desde variables de entorno
    - `company_name`: Nombre de la empresa para footer
    - `logo_url`: URL del logo corporativo
    - `support_email`: Email de contacto para soporte
    - `website_url`: URL por defecto si no se especifica
    
    Args:
        request (WaitlistEmailRequest): **Datos del usuario** con email obligatorio,
                                      ofertas de interés y personalización opcional.
    
    Returns:
        WaitlistEmailResponse: **Confirmación detallada** del envío con metadatos
                              completos, tipo de mensaje y texto de ofertas generado.
    
    Example:
        ```json
        // Múltiples ofertas
        {
            "email": "usuario@empresa.com",
            "user_name": "María González",
            "website_url": "https://miapp.com",
            "offerings": ["CRM Avanzado", "Sistema de Inventarios", "Analytics Pro"]
        }
        
        // Una sola oferta
        {
            "email": "juan@startup.com",
            "user_name": "Juan Pérez",
            "offerings": ["CRM Avanzado"]
        }
        
        // Sin ofertas específicas
        {
            "email": "ana@empresa.com",
            "offerings": []
        }
        ```
    
    Note:
        - Si `offerings` está vacío, se usa mensaje genérico de plataforma
        - Si tiene 1 elemento, se personaliza para esa oferta específica
        - Si tiene múltiples elementos, se listan todas separadas por comas
        - Máximo 10 ofertas permitidas, cada una con máximo 100 caracteres
        - El tipo de mensaje se incluye en la respuesta para debugging
        - Todos los elementos de branding se toman automáticamente de variables de entorno
    """
    
    try:
        # Enviar email de confirmación de waitlist
        response = controller.send_waitlist_email(request)
        
        # Si el envío falló, lanzar HTTPException
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        # Re-lanzar HTTPExceptions tal como están
        raise
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"[ERROR] Error inesperado en endpoint send_confirmation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )