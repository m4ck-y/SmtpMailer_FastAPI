from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Configuración de la aplicación SmtpMailer FastAPI.
    
    Carga variables de entorno desde archivo .env y proporciona valores por defecto
    para desarrollo. Todas las configuraciones SMTP son obligatorias para el
    funcionamiento correcto del servicio de envío de correos.
    """
    
    # === CONFIGURACIÓN DE LA API ===
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # === CONFIGURACIÓN SMTP (OBLIGATORIAS) ===
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str = "SmtpMailer API"
    
    # === CONFIGURACIÓN DE SEGURIDAD ===
    API_KEY_ENABLED: bool = False
    API_KEY: Optional[str] = None
    RATE_LIMIT_ENABLED: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 100
    MAX_REQUESTS_PER_HOUR: int = 1000
    
    # === CONFIGURACIÓN DE CORS ===
    ALLOWED_ORIGINS: str = "*"
    ALLOWED_METHODS: str = "GET,POST,PUT,DELETE,OPTIONS"
    ALLOWED_HEADERS: str = "*"
    
    # === CONFIGURACIÓN DE PLANTILLAS ===
    COMPANY_NAME: str = "Mi Empresa"
    COMPANY_LOGO_URL: Optional[str] = None
    SUPPORT_EMAIL: Optional[str] = None
    WEBSITE_URL: Optional[str] = None
    
    # === CONFIGURACIÓN DE CACHE ===
    CACHE_TTL_SECONDS: int = 300  # 5 minutos
    CACHE_ENABLED: bool = True
    
    # === CONFIGURACIÓN DE TIMEOUTS ===
    SMTP_TIMEOUT: int = 30
    REQUEST_TIMEOUT: int = 60
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Instancia global de configuración
settings = Settings()