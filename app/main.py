from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.otp.router import router_otp, TAG_OTP
from app.waitlist.router import router_waitlist, TAG_WAITLIST

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="🚀 SmtpMailer FastAPI - Email Service API",
    version="1.0.0",
    description="""
API RESTful stateless para envío de correos electrónicos con Gmail SMTP.

## 📧 Funcionalidades Principales
- **Envío de códigos OTP** - Autenticación de dos factores
- **Correos de bienvenida** - Onboarding de usuarios
- **Recuperación de contraseña** - Enlaces y códigos seguros
- **Emails personalizados** - Plantillas HTML responsivas

## 🚀 Características Técnicas
- **Configuración por variables de entorno** - Sin base de datos
- **Validación automática** - Pydantic v2 para datos de entrada
- **Operaciones asíncronas** - Alta performance y concurrencia
- **Seguridad integrada** - Rate limiting y headers seguros

## 🔗 Enlaces
- **Repositorio:** [github.com/m4ck-y/SmtpMailer_FastAPI](https://github.com/m4ck-y/SmtpMailer_FastAPI)
- **Soporte:** [GitHub Issues](https://github.com/m4ck-y/SmtpMailer_FastAPI/issues)
""",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[TAG_OTP, TAG_WAITLIST]
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS.split(","),
    allow_headers=settings.ALLOWED_HEADERS.split(","),
)

@app.get("/")
async def root():
    """Endpoint raíz que retorna información básica de la API."""
    return {
        "message": "SmtpMailer FastAPI - Email Service",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check básico del servicio."""
    return {
        "status": "healthy",
        "service": "SmtpMailer FastAPI",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "smtp_configured": bool(settings.SMTP_HOST and settings.SMTP_USERNAME and settings.SMTP_PASSWORD)
    }


app.include_router(router_otp)
app.include_router(router_waitlist)