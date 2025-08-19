from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional


class OTPEmailRequest(BaseModel):
    """
    Modelo de solicitud para envío de email OTP simplificado.
    
    Configuración mínima requerida para envío de OTP. El nombre de la aplicación
    y logo se toman automáticamente de las variables de entorno configuradas,
    simplificando la integración y manteniendo consistencia en el branding.
    
    Attributes:
        email (EmailStr): **Dirección de correo electrónico** del destinatario.
                         Validación automática RFC-compliant.
        code (str): **Código OTP alfanumérico** de verificación temporal.
                   Entre 4-8 caracteres (letras, números o combinación).
        expiry_minutes (Optional[int]): **Tiempo de expiración** en minutos.
                                       Si es 0 o None, no se muestra mensaje de expiración.
        redirect_url (Optional[str]): **URL de redirección automática**.
                                     Si no se proporciona, no se muestra botón.
    
    Note:
        - `app_name` se toma de la variable de entorno APP_NAME
        - `logo_url` se toma de la variable de entorno COMPANY_LOGO_URL
        - Esto garantiza consistencia en el branding y simplifica la integración
    
    Example:
        >>> # Caso típico - solo datos esenciales
        >>> request = OTPEmailRequest(
        ...     email="usuario@ejemplo.com",
        ...     code="A1B2C3",
        ...     expiry_minutes=15,
        ...     redirect_url="https://app.com/verify?token=abc123"
        ... )
        >>> 
        >>> # Caso mínimo - solo email y código
        >>> request_minimal = OTPEmailRequest(
        ...     email="usuario@ejemplo.com",
        ...     code="XYZ789"
        ... )
    """
    
    email: EmailStr = Field(
        ...,
        description="**Email del destinatario** - Debe ser RFC-compliant",
        example="usuario@ejemplo.com"
    )
    
    code: str = Field(
        ...,
        min_length=4,
        max_length=8,
        description="**Código OTP** - Entre 4 y 8 caracteres (alfanumérico)",
        example="A1B2C3"
    )
    

    
    expiry_minutes: Optional[int] = Field(
        None,
        ge=0,
        le=1440,  # Máximo 24 horas
        description="**Tiempo de expiración** en minutos. Si es 0 o None, no se muestra mensaje",
        example=10
    )
    
    redirect_url: Optional[str] = Field(
        None,
        max_length=2048,
        description="**URL de redirección** - Botón opcional para redirigir al usuario automáticamente",
        example="https://app.com/dashboard?verified=true"
    )
    
    @validator('redirect_url')
    def validate_redirect_url(cls, v):
        """Valida que la URL de redirección tenga formato correcto si se proporciona."""
        if v is not None and v.strip():
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('URL de redirección debe comenzar con http:// o https://')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "code": "A1B2C3",
                "expiry_minutes": 10,
                "redirect_url": "https://app.com/dashboard?verified=true"
            }
        }


class OTPEmailResponse(BaseModel):
    """
    Respuesta estándar para operaciones de envío de email OTP.
    
    Proporciona información detallada sobre el resultado del envío incluyendo
    timestamps y configuración aplicada para debugging y confirmación.
    
    Attributes:
        success (bool): **Estado del envío** - True si fue exitoso.
        message (str): **Mensaje descriptivo** del resultado.
        email_sent_to (str): **Email de destino** - Confirmación del destinatario.
        timestamp (str): **Timestamp ISO** - Momento exacto del envío.
        expiry_minutes (Optional[int]): **Minutos de expiración** aplicados.
        has_verification_button (bool): **Indica si se incluyó botón** de verificación.
        logo_used (str): **URL del logo** utilizado en el email.
    """
    
    success: bool = Field(
        ...,
        description="**Estado del envío** - True si fue exitoso"
    )
    
    message: str = Field(
        ...,
        description="**Mensaje descriptivo** - Detalles del resultado"
    )
    
    email_sent_to: str = Field(
        ...,
        description="**Email de destino** - Confirmación del destinatario"
    )
    
    timestamp: str = Field(
        ...,
        description="**Timestamp ISO** - Momento exacto del envío"
    )
    
    expiry_minutes: Optional[int] = Field(
        None,
        description="**Minutos de expiración** - Configuración aplicada"
    )
    
    has_verification_button: bool = Field(
        ...,
        description="**Botón de verificación** - True si se incluyó en el email"
    )
    
    logo_used: str = Field(
        ...,
        description="**URL del logo** - Logo utilizado en el email"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Código OTP enviado exitosamente",
                "email_sent_to": "usuario@ejemplo.com",
                "timestamp": "2025-01-19T10:30:00Z",
                "expiry_minutes": 10,
                "has_verification_button": True,
                "logo_used": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5mug1kZAbRtSexOlAnCSRDudlfe-GKxYfQA&s"
            }
        }