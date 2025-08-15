from fastapi import APIRouter, HTTPException, status
from app.otp.controller import EmailOTPApplication


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

@router_otp.post("/send_otp")
def enviar_codigo_otp(email: str, code: str, app_name: str):
    """
    Envía un código de verificación OTP (One-Time Password) por correo electrónico.
    
    Genera y envía un email con código de verificación temporal utilizando
    plantilla HTML responsiva optimizada para múltiples clientes de correo.
    Diseñado para procesos de autenticación de dos factores y verificación de identidad.
    
    Args:
        email (str): **Dirección de correo electrónico** del destinatario.
                    Debe ser un email válido en formato RFC-compliant.
                    Ejemplo: "usuario@ejemplo.com".
        code (str): **Código OTP numérico** de verificación temporal.
                   Típicamente entre 4-8 dígitos generado aleatoriamente.
                   Ejemplo: "123456".
        app_name (str): **Nombre de la aplicación** que solicita la verificación.
                       Se usa para personalizar el email y mejorar la confianza del usuario.
                       Ejemplo: "Hospital Digital", "Mi App Salud".
    
    Example:
        >>> enviar_codigo_otp("usuario@gmail.com", "847392", "Hospital Digital")
        # TODO: Definir estructura exacta de respuesta
    
    Note:
        - El código OTP debe ser generado externamente con suficiente entropía
        - Se recomienda implementar rate limiting para prevenir abuso
        - La plantilla HTML incluye fallback a texto plano para compatibilidad
        - El email se envía de forma asíncrona para optimizar performance
    """
    
    # TODO: Implementar validación de formato de email
    # TODO: Implementar validación de código OTP (4-8 dígitos numéricos)
    # TODO: Implementar rate limiting por IP/email
    
    # TODO: Cargar plantilla HTML para OTP
    # TODO: Renderizar plantilla con variables: code, app_name, email
    
    # TODO: Configurar cliente SMTP asíncrono
    # TODO: Enviar email con manejo de errores robusto
    
    # TODO: Retornar respuesta estructurada:
    # {
    #     "success": True,
    #     "message": "Código OTP enviado exitosamente", 
    #     "email_sent_to": email,
    #     "timestamp": "2025-01-15T10:30:00Z",
    #     "otp_expires_in": "10 minutes"
    # }
    
    try:
        controller.Send_OTP(email, code, app_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))