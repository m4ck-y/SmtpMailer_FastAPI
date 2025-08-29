from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List


class WaitlistEmailRequest(BaseModel):
    """
    Modelo de solicitud para envío de email de confirmación de waitlist.
    
    Configuración para notificar al usuario que su correo ha sido registrado
    exitosamente en la lista de espera. Permite especificar múltiples ofertas
    (productos/servicios) para personalizar el mensaje de confirmación.
    
    Attributes:
        email (EmailStr): **Dirección de correo electrónico** del usuario registrado.
                         Validación automática RFC-compliant.
        user_name (Optional[str]): **Nombre del usuario** para personalización.
                                  Si no se proporciona, se usa "Usuario".
        website_url (Optional[str]): **URL del sitio web** para el botón de visita.
                                    Si no se proporciona, se usa la URL por defecto.
        offerings (List[str]): **Lista de ofertas** (productos/servicios) para los que
                              se registra el usuario. Personaliza el mensaje según cantidad.
    
    Note:
        - El branding se toma automáticamente de variables de entorno
        - Si `offerings` está vacío, se usa mensaje genérico de plataforma
        - Si tiene 1 elemento, se personaliza para esa oferta específica
        - Si tiene múltiples elementos, se listan todas las ofertas
    
    Example:
        >>> # Caso con múltiples ofertas
        >>> request = WaitlistEmailRequest(
        ...     email="usuario@ejemplo.com",
        ...     user_name="Juan Pérez",
        ...     website_url="https://miapp.com",
        ...     offerings=["CRM Avanzado", "Sistema de Inventarios", "Analytics Pro"]
        ... )
        >>> 
        >>> # Caso con una sola oferta
        >>> request_single = WaitlistEmailRequest(
        ...     email="usuario@ejemplo.com",
        ...     offerings=["CRM Avanzado"]
        ... )
        >>> 
        >>> # Caso sin ofertas específicas (plataforma general)
        >>> request_platform = WaitlistEmailRequest(
        ...     email="usuario@ejemplo.com",
        ...     offerings=[]
        ... )
    """
    
    email: EmailStr = Field(
        ...,
        description="**Email del usuario** - Dirección registrada en la waitlist",
        example="usuario@ejemplo.com"
    )
    
    user_name: Optional[str] = Field(
        None,
        max_length=100,
        description="**Nombre del usuario** - Para personalización del email",
        example="Juan Pérez"
    )
    
    website_url: Optional[str] = Field(
        None,
        max_length=2048,
        description="**URL del sitio web** - Para el botón de visita",
        example="https://miapp.com"
    )
    
    offerings: List[str] = Field(
        default_factory=list,
        max_items=10,
        description="**Lista de ofertas** - Productos/servicios de interés del usuario",
        example=["CRM Avanzado", "Sistema de Inventarios", "Analytics Pro"]
    )
    
    @validator('website_url')
    def validate_website_url(cls, v):
        """Valida que la URL del sitio web tenga formato correcto si se proporciona."""
        if v is not None and v.strip():
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('URL del sitio web debe comenzar con http:// o https://')
        return v
    
    @validator('offerings')
    def validate_offerings(cls, v):
        """Valida que las ofertas no estén vacías y tengan longitud apropiada."""
        if v:
            for offering in v:
                if not offering or not offering.strip():
                    raise ValueError('Las ofertas no pueden estar vacías')
                if len(offering.strip()) > 100:
                    raise ValueError('Cada oferta debe tener máximo 100 caracteres')
        return [offering.strip() for offering in v if offering.strip()]
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Múltiples ofertas",
                    "value": {
                        "email": "usuario@ejemplo.com",
                        "user_name": "Juan Pérez",
                        "website_url": "https://miapp.com",
                        "offerings": ["CRM Avanzado", "Sistema de Inventarios", "Analytics Pro"]
                    }
                },
                {
                    "name": "Una sola oferta",
                    "value": {
                        "email": "maria@empresa.com",
                        "user_name": "María González",
                        "offerings": ["CRM Avanzado"]
                    }
                },
                {
                    "name": "Sin ofertas específicas",
                    "value": {
                        "email": "carlos@startup.com",
                        "user_name": "Carlos Ruiz",
                        "offerings": []
                    }
                }
            ]
        }


class WaitlistEmailResponse(BaseModel):
    """
    Respuesta estándar para operaciones de envío de email de waitlist.
    
    Proporciona información detallada sobre el resultado del envío incluyendo
    timestamps, configuración aplicada y detalles de personalización para
    debugging y confirmación.
    
    Attributes:
        success (bool): **Estado del envío** - True si fue exitoso.
        message (str): **Mensaje descriptivo** del resultado.
        email_sent_to (str): **Email de destino** - Confirmación del destinatario.
        timestamp (str): **Timestamp ISO** - Momento exacto del envío.
        user_name (str): **Nombre utilizado** - Nombre aplicado en el email.
        has_website_button (bool): **Indica si se incluyó botón** del sitio web.
        logo_used (str): **URL del logo** utilizado en el email.
        offerings_count (int): **Cantidad de ofertas** - Número de ofertas especificadas.
        message_type (str): **Tipo de mensaje** - single/multiple/platform según ofertas.
        offerings_text (str): **Texto de ofertas** - Texto generado para las ofertas.
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
    
    user_name: str = Field(
        ...,
        description="**Nombre utilizado** - Nombre aplicado en el email"
    )
    
    has_website_button: bool = Field(
        ...,
        description="**Botón del sitio web** - True si se incluyó en el email"
    )
    
    logo_used: str = Field(
        ...,
        description="**URL del logo** - Logo utilizado en el email"
    )
    
    offerings_count: int = Field(
        ...,
        description="**Cantidad de ofertas** - Número de ofertas especificadas"
    )
    
    message_type: str = Field(
        ...,
        description="**Tipo de mensaje** - single/multiple/platform según ofertas"
    )
    
    offerings_text: str = Field(
        ...,
        description="**Texto de ofertas** - Texto generado para las ofertas en el email"
    )
    
    offerings_text_html: str = Field(
        ...,
        description="**Texto de ofertas HTML** - Texto con formato HTML para ofertas en negrita"
    )
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Respuesta con múltiples ofertas",
                    "value": {
                        "success": True,
                        "message": "Email de confirmación de waitlist enviado exitosamente",
                        "email_sent_to": "usuario@ejemplo.com",
                        "timestamp": "2025-01-19T10:30:00Z",
                        "user_name": "Juan Pérez",
                        "has_website_button": True,
                        "logo_used": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5mug1kZAbRtSexOlAnCSRDudlfe-GKxYfQA&s",
                        "offerings_count": 3,
                        "message_type": "multiple",
                        "offerings_text": "CRM Avanzado, Sistema de Inventarios, Analytics Pro",
                        "offerings_text_html": "<strong>CRM Avanzado</strong>, <strong>Sistema de Inventarios</strong>, <strong>Analytics Pro</strong>"
                    }
                },
                {
                    "name": "Respuesta con una oferta",
                    "value": {
                        "success": True,
                        "message": "Email de confirmación de waitlist enviado exitosamente",
                        "email_sent_to": "maria@empresa.com",
                        "timestamp": "2025-01-19T10:30:00Z",
                        "user_name": "María González",
                        "has_website_button": False,
                        "logo_used": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5mug1kZAbRtSexOlAnCSRDudlfe-GKxYfQA&s",
                        "offerings_count": 1,
                        "message_type": "single",
                        "offerings_text": "CRM Avanzado",
                        "offerings_text_html": "<strong>CRM Avanzado</strong>"
                    }
                },
                {
                    "name": "Respuesta sin ofertas específicas",
                    "value": {
                        "success": True,
                        "message": "Email de confirmación de waitlist enviado exitosamente",
                        "email_sent_to": "carlos@startup.com",
                        "timestamp": "2025-01-19T10:30:00Z",
                        "user_name": "Carlos Ruiz",
                        "has_website_button": True,
                        "logo_used": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5mug1kZAbRtSexOlAnCSRDudlfe-GKxYfQA&s",
                        "offerings_count": 0,
                        "message_type": "platform",
                        "offerings_text": "nuestra plataforma",
                        "offerings_text_html": "nuestra plataforma"
                    }
                }
            ]
        }