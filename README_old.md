# 📧 SmtpMailer_FastAPI

## 🧩 Descripción General

**SmtpMailer_FastAPI** es una API RESTful robusta y configurable para el envío de correos electrónicos utilizando cualquier proveedor SMTP (Gmail, Outlook, SendGrid, etc.). Diseñada con arquitectura limpia y patrones de diseño modernos para aplicaciones de producción.

La API permite enviar diferentes tipos de correos electrónicos como códigos OTP, mensajes de bienvenida, recuperación de contraseña y emails personalizados, con soporte para plantillas HTML y configuración dinámica de credenciales SMTP.

## 🚀 Características Principales

| Funcionalidad | Descripción |
|---------------|-------------|
| 🔑 **Configuración SMTP Dinámica** | Configuración de credenciales SMTP en tiempo de ejecución |
| 🧱 **Endpoints Especializados** | Endpoints específicos para cada tipo de correo |
| 🎨 **Sistema de Plantillas** | Soporte para plantillas HTML personalizables |
| 🛠️ **API RESTful** | Diseño REST puro con documentación OpenAPI automática |
| 🔒 **Seguridad Integrada** | Validación de entrada, rate limiting y headers de seguridad |
| 📊 **Logging y Monitoreo** | Sistema de logs estructurado y métricas de performance |
| ⚡ **Alta Performance** | Optimizado para alto throughput con cache inteligente |

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico
- **Framework:** FastAPI 0.104+
- **Lenguaje:** Python 3.12+
- **SMTP:** smtplib nativo + aiosmtplib para operaciones asíncronas
- **Validación:** Pydantic v2 para validación de datos
- **Documentación:** OpenAPI/Swagger automático
- **Logging:** Logging estructurado compatible con sistemas de monitoreo

### Principios de Diseño
- **Clean Architecture** - Separación estricta de responsabilidades
- **SOLID Principles** - Código mantenible y extensible
- **RESTful Design** - APIs semánticamente correctas
- **Security First** - Seguridad integrada desde el diseño
- **Performance Oriented** - Optimizado para alta concurrencia

## 📋 Endpoints de la API

### 🔧 Configuración SMTP

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/smtp/configure` | POST | Configura las credenciales SMTP del servicio |
| `/smtp/status` | GET | Verifica la configuración SMTP actual y conectividad |
| `/smtp/test` | POST | Envía un correo de prueba para validar configuración |

### 📤 Envío de Correos

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/emails/send` | POST | Envía un correo genérico con contenido personalizado |
| `/emails/send-otp` | POST | Envía código OTP con plantilla predefinida |
| `/emails/welcome` | POST | Envía correo de bienvenida personalizable |
| `/emails/recovery` | POST | Envía enlace/código de recuperación de contraseña |
| `/emails/custom` | POST | Envía correo con plantilla HTML personalizada |

### 📚 Utilidades y Administración

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/emails/logs` | GET | Lista historial de correos enviados (paginado) |
| `/emails/logs/{id}` | GET | Detalle específico de un correo enviado |
| `/templates` | GET | Lista plantillas disponibles en el sistema |
| `/templates/{type}` | GET | Obtiene plantilla específica por tipo |
| `/health` | GET | Health check básico del servicio |
| `/health/detailed` | GET | Health check detallado con dependencias |

## 🔧 Instalación y Configuración

### Requisitos del Sistema
- Python 3.12 o superior
- uv (Python package manager moderno)
- Acceso a servidor SMTP (Gmail, Outlook, SendGrid, etc.)

### Instalación Rápida

```bash
# Clonar el repositorio
git clone git@github.com:m4ck-y/SmtpMailer_FastAPI.git
cd SmtpMailer_FastAPI

# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sincronizar dependencias (crea automáticamente el entorno virtual)
uv sync

# Ejecutar la aplicación
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Variables de Entorno

```bash
# Configuración básica
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
PORT=8000

# Configuración de seguridad (opcional)
API_KEY_ENABLED=false
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=100

# Configuración de cache (opcional)
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300
```

## 📖 Uso de la API

### Configuración Inicial SMTP

```bash
# Configurar credenciales SMTP
curl -X POST "http://localhost:8000/smtp/configure" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "tu-email@gmail.com",
    "password": "tu-app-password",
    "use_tls": true
  }'
```

### Envío de Correo OTP

```bash
# Enviar código OTP
curl -X POST "http://localhost:8000/emails/send-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "usuario@ejemplo.com",
    "otp_code": "123456",
    "user_name": "Juan Pérez",
    "expires_in_minutes": 10
  }'
```

### Envío de Correo de Bienvenida

```bash
# Enviar correo de bienvenida
curl -X POST "http://localhost:8000/emails/welcome" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "nuevo-usuario@ejemplo.com",
    "user_name": "María González",
    "company_name": "Mi Empresa",
    "login_url": "https://mi-app.com/login"
  }'
```

## 🔒 Seguridad

### Características de Seguridad Implementadas
- **Validación de entrada** con Pydantic para todos los endpoints
- **Rate limiting** configurable por IP y endpoint
- **Headers de seguridad** (CORS, CSP, HSTS)
- **Sanitización de datos** para prevenir inyecciones
- **Logging de seguridad** para auditoría de accesos
- **Configuración segura** de credenciales SMTP

### Mejores Prácticas Recomendadas
- Usar contraseñas de aplicación en lugar de contraseñas principales
- Configurar CORS apropiadamente para tu dominio
- Implementar autenticación API key para producción
- Monitorear logs de seguridad regularmente
- Mantener credenciales SMTP en variables de entorno seguras

## 📊 Monitoreo y Observabilidad

### Métricas Disponibles
- Tiempo de respuesta por endpoint
- Tasa de éxito/error de envío de correos
- Uso de memoria y CPU
- Estadísticas de rate limiting
- Métricas de conectividad SMTP

### Logging Estructurado
```json
{
  "timestamp": "2025-01-13T10:30:00Z",
  "level": "INFO",
  "service": "smtp-mailer-api",
  "endpoint": "/emails/send-otp",
  "status_code": 200,
  "response_time_ms": 150,
  "email_sent": true,
  "recipient": "user@example.com"
}
```

## 🚀 Despliegue

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  smtp-mailer-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

## 🧪 Testing

```bash
# Ejecutar tests unitarios
pytest tests/ -v

# Ejecutar tests con coverage
pytest tests/ --cov=app --cov-report=html

# Ejecutar tests de integración
pytest tests/integration/ -v
```

## 📚 Documentación de la API

Una vez que la aplicación esté ejecutándose, la documentación interactiva estará disponible en:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Estándares de Código
- Seguir PEP 8 para estilo de código Python
- Documentar todas las funciones públicas con docstrings
- Incluir tests para nuevas funcionalidades
- Mantener cobertura de tests > 80%

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

- **Issues:** [GitHub Issues](https://github.com/m4ck-y/SmtpMailer_FastAPI/issues)
- **Documentación:** [Wiki del Proyecto](https://github.com/m4ck-y/SmtpMailer_FastAPI/wiki)
- **Email:** soporte@tu-dominio.com

---

**SmtpMailer_FastAPI** - Solución profesional para envío de correos electrónicos con FastAPI 🚀