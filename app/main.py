from fastapi import FastAPI

app = FastAPI(
    title="🚀 SmtpMailer FastAPI - Email Service API",
    version="1.0.0",
    #TODO: simpliicar la descripcion, porque caundo de descpiegue va estar configurado solo para gmail, y se daran de alta determinados enpoins
    description="""
API RESTful stateless para envío de correos electrónicos con soporte multi-proveedor SMTP.

SmtpMailer FastAPI es una solución moderna diseñada para aplicaciones que requieren envío de emails 
confiable y escalable sin la complejidad de gestionar bases de datos o estados persistentes.

## 📋 Características Principales
- **Configuración por variables de entorno** - Sin persistencia de datos, ideal para contenedores
- **Soporte multi-proveedor** - Gmail, Outlook, SendGrid, Mailgun y proveedores SMTP personalizados
- **Plantillas HTML responsivas** - Sistema de templates con Jinja2 para emails profesionales
- **Arquitectura stateless** - Optimizada para microservicios y escalabilidad horizontal
- **Validación robusta** - Pydantic v2 para validación automática de datos de entrada
- **Seguridad integrada** - Rate limiting, headers de seguridad y sanitización de datos

## 🎯 Casos de Uso Principales
- **Códigos OTP** - Autenticación de dos factores con plantillas personalizables
- **Correos de bienvenida** - Onboarding de usuarios con branding personalizado
- **Recuperación de contraseña** - Enlaces seguros y códigos de recuperación
- **Emails transaccionales** - Confirmaciones, notificaciones y alertas del sistema
- **Comunicaciones masivas** - Envío eficiente con procesamiento asíncrono

## 🚀 Stack Tecnológico
- **FastAPI 0.104+** - Framework moderno con documentación automática
- **Pydantic v2** - Validación de datos y serialización de alta performance
- **aiosmtplib** - Cliente SMTP asíncrono para operaciones concurrentes
- **Jinja2** - Motor de plantillas HTML para emails responsivos
- **Python 3.12+** - Type hints completos y características modernas del lenguaje

## 🔒 Seguridad y Performance
- ✅ **Operaciones asíncronas** - Envío concurrente de múltiples emails
- ✅ **Rate limiting** - Protección contra abuso y spam
- ✅ **Headers de seguridad** - CORS, CSP, HSTS configurados automáticamente
- ✅ **Logging estructurado** - Monitoreo y debugging eficiente

## 🔗 Enlaces Útiles
- **Repositorio:** [github.com/m4ck-y/SmtpMailer_FastAPI](https://github.com/m4ck-y/SmtpMailer_FastAPI)
- **Documentación:** Ver README.md para guías de configuración detalladas
- **Soporte:** [GitHub Issues](https://github.com/m4ck-y/SmtpMailer_FastAPI/issues)
""",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}