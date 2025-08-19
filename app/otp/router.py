from fastapi import APIRouter, HTTPException, status
from app.otp.controller import EmailOTPApplication
from app.otp.models import OTPEmailRequest, OTPEmailResponse

controller = EmailOTPApplication()

MODULE_NAME = "email"

router_otp = APIRouter(
    prefix=f"/{MODULE_NAME}",
    tags=[MODULE_NAME])

TAG_OTP = {
    "name": MODULE_NAME,
    "description": """
- 🔐 **Códigos OTP** - Envío de códigos de verificación seguros
- 🎯 **Funcionalidades:** Generación y envío de códigos temporales para 2FA
- 🚀 **Casos de uso:** Registro, login seguro, recuperación de cuenta  
- 📧 **Características:** HTML responsivo, rate limiting, validación RFC
- ⚡ **Seguridad:** Códigos aleatorios, expiración configurable, logging completo
"""
}

@router_otp.post("/send_otp", response_model=OTPEmailResponse)
def enviar_codigo_otp(request: OTPEmailRequest) -> OTPEmailResponse:
    """
    Envía un código de verificación OTP (One-Time Password) por correo electrónico con configuración avanzada.
    
    Genera y envía un email con código de verificación temporal utilizando plantilla HTML responsiva
    con personalización completa: tiempo de expiración configurable, verificación automática opcional
    y logo personalizable. Optimizado para múltiples clientes de correo y casos de uso empresariales.
    
    ### 🔐 Características de Seguridad:
    - Código OTP con validación de formato (4-8 caracteres alfanuméricos)
    - Tiempo de expiración configurable (0-1440 minutos)
    - Validación RFC-compliant de direcciones de email
    - Headers de seguridad y logging completo de operaciones
    
    ### 📧 Personalización Automática:
    - **Logo y branding:** Configurados automáticamente desde variables de entorno
    - **Redirección automática:** Botón opcional con URL de redirección
    - **Tiempo de expiración:** Configurable o sin mostrar si es 0/None
    - **Consistencia:** Branding uniforme en todos los emails
    
    ### ⚡ Casos de Uso:
    - Autenticación de dos factores (2FA)
    - Verificación de registro de usuarios
    - Recuperación de contraseñas
    - Confirmación de transacciones críticas
    
    Args:
        request (OTPEmailRequest): **Configuración completa del email OTP** con todos los parámetros
                                  de personalización y comportamiento.
    
    Returns:
        OTPEmailResponse: **Respuesta detallada** con estado del envío, metadatos de configuración
                         aplicada y información para debugging.
    
    Example:
        ```json
        {
            "email": "usuario@hospital.com",
            "code": "A1B2C3",
            "expiry_minutes": 15,
            "redirect_url": "https://app.hospital.com/dashboard?verified=true"
        }
        ```
    
    Note:
        - Si `expiry_minutes` es 0 o None, no se muestra mensaje de expiración
        - Si `redirect_url` es None o vacía, no se muestra botón de redirección
        - `app_name` y `logo_url` se toman automáticamente de las variables de entorno
        - Esto garantiza consistencia en el branding y simplifica la integración
        - Las URLs se validan automáticamente (deben comenzar con http/https)
    """
    
    try:
        # Enviar email OTP con configuración avanzada
        response = controller.send_otp_email(request)
        
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
        print(f"[ERROR] Error inesperado en endpoint send_otp: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router_otp.post("/send_otp_legacy")
def enviar_codigo_otp_legacy(email: str, code: str, app_name: str):
    """
    Endpoint legacy para envío de OTP con parámetros simples.
    
    DEPRECATED: Este endpoint se mantiene para compatibilidad hacia atrás.
    Se recomienda usar `/send_otp` con el modelo OTPEmailRequest completo.
    
    Args:
        email (str): Dirección de correo electrónico del destinatario.
        code (str): Código OTP alfanumérico (4-8 caracteres).
        app_name (str): Nombre de la aplicación.
    
    Returns:
        dict: Respuesta básica de éxito o error.
    """
    try:
        # Crear request básico para compatibilidad (app_name ya no se usa)
        request = OTPEmailRequest(
            email=email,
            code=code
        )
        
        # Usar el controlador nuevo
        response = controller.send_otp_email(request)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.message
            )
        
        # Retornar formato simplificado para compatibilidad
        return {
            "success": True,
            "message": "Código OTP enviado exitosamente",
            "email_sent_to": email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error en endpoint legacy: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )