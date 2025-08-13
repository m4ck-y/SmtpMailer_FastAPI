# 📧 SmtpMailer_FastAPI

## 🧩 Descripción General

**SmtpMailer_FastAPI** es una API RESTful stateless para el envío de correos electrónicos utilizando cualquier proveedor SMTP (Gmail, Outlook, SendGrid, etc.). Diseñada con arquitectura limpia y configuración basada en variables de entorno para aplicaciones de producción.

La API permite enviar diferentes tipos de correos electrónicos como códigos OTP, mensajes de bienvenida, recuperación de contraseña y emails personalizados, con soporte para plantillas HTML. **No requiere base de datos** ya que toda la configuración se maneja a través de variables de entorno.

## 🚀 Características Principales

| Funcionalidad | Descripción |
|---------------|-------------|
| � **Configuuración por Variables de Entorno** | Configuración SMTP mediante variables de entorno o contenedor |
| 🧱 **Endpoints Especializados** | Endpoints específicos para cada tipo de correo |
| 🎨 **Sistema de Plantillas** | Soporte para plantillas HTML personalizables |
| 🛠️ **API RESTful Stateless** | Sin base de datos, configuración por entorno |
| 🔒 **Seguridad Integrada** | Validación de entrada, rate limiting y headers de seguridad |
| 📊 **Logging y Monitoreo** | Sistema de logs estructurado y métricas de performance |
| ⚡ **Alta Performance** | Optimizado para alto throughput sin persistencia |

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico
- **Framework:** FastAPI 0.104+
- **Lenguaje:** Python 3.12+
- **SMTP:** smtplib nativo + aiosmtplib para operaciones asíncronas
- **Validación:** Pydantic v2 para validación de datos
- **Configuración:** Variables de entorno (sin base de datos)
- **Documentación:** OpenAPI/Swagger automático
- **Logging:** Logging estructurado compatible con sistemas de monitoreo

### Principios de Diseño
- **Stateless Architecture** - Sin persistencia de datos, configuración por entorno
- **12-Factor App** - Configuración externa, portabilidad entre entornos
- **Clean Architecture** - Separación estricta de responsabilidades
- **RESTful Design** - APIs semánticamente correctas
- **Security First** - Seguridad integrada desde el diseño

## 📋 Endpoints de la API

### 🔧 Estado y Configuración

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/smtp/status` | GET | Verifica la configuración SMTP actual y conectividad |
| `/smtp/test` | POST | Envía un correo de prueba para validar configuración |
| `/health` | GET | Health check básico del servicio |
| `/health/detailed` | GET | Health check detallado con dependencias SMTP |

### 📤 Envío de Correos

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/emails/send` | POST | Envía un correo genérico con contenido personalizado |
| `/emails/send-otp` | POST | Envía código OTP con plantilla predefinida |
| `/emails/welcome` | POST | Envía correo de bienvenida personalizable |
| `/emails/recovery` | POST | Envía enlace/código de recuperación de contraseña |
| `/emails/custom` | POST | Envía correo con plantilla HTML personalizada |

### 📚 Utilidades

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/templates` | GET | Lista plantillas disponibles en el sistema |
| `/templates/{type}` | GET | Obtiene plantilla específica por tipo |

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

# Configurar variables de entorno (ver sección siguiente)
cp .env.example .env
# Editar .env con tus credenciales SMTP

# Ejecutar la aplicación
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Variables de Entorno Requeridas

```bash
# === CONFIGURACIÓN SMTP (OBLIGATORIAS) ===
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=tu-email@gmail.com
SMTP_FROM_NAME="Mi Aplicación"

# === CONFIGURACIÓN BÁSICA ===
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
PORT=8000

# === CONFIGURACIÓN DE SEGURIDAD (OPCIONAL) ===
API_KEY_ENABLED=false
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=100

# === CONFIGURACIÓN DE PLANTILLAS (OPCIONAL) ===
COMPANY_NAME="Mi Empresa"
COMPANY_LOGO_URL="https://mi-empresa.com/logo.png"
SUPPORT_EMAIL="soporte@mi-empresa.com"
```

### Ejemplo de Configuración para Diferentes Proveedores

#### Gmail
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password  # Usar App Password, no contraseña normal
SMTP_USE_TLS=true
```

#### Outlook/Hotmail
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@outlook.com
SMTP_PASSWORD=tu-contraseña
SMTP_USE_TLS=true
```

#### SendGrid
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=tu-sendgrid-api-key
SMTP_USE_TLS=true
```

## 📖 Uso de la API

### Verificar Estado del Servicio

```bash
# Verificar configuración SMTP
curl -X GET "http://localhost:8000/smtp/status"

# Respuesta esperada:
{
  "status": "connected",
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 587,
  "from_email": "tu-email@gmail.com",
  "timestamp": "2025-01-13T10:30:00Z"
}
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
    "login_url": "https://mi-app.com/login"
  }'
```

### Envío de Correo Genérico

```bash
# Enviar correo personalizado
curl -X POST "http://localhost:8000/emails/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "destinatario@ejemplo.com",
    "subject": "Asunto del correo",
    "html_content": "<h1>Hola</h1><p>Este es un correo de prueba.</p>",
    "text_content": "Hola, este es un correo de prueba."
  }'
```

## 🚀 Despliegue

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar archivos de configuración
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de ejecución
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
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
      # Configuración SMTP
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_USERNAME=tu-email@gmail.com
      - SMTP_PASSWORD=tu-app-password
      - SMTP_USE_TLS=true
      - SMTP_FROM_EMAIL=tu-email@gmail.com
      - SMTP_FROM_NAME=Mi Aplicación
      
      # Configuración de la aplicación
      - ENVIRONMENT=production
      - DEBUG=false
      - LOG_LEVEL=INFO
      - PORT=8000
      
      # Configuración de empresa
      - COMPANY_NAME=Mi Empresa
      - SUPPORT_EMAIL=soporte@mi-empresa.com
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smtp-mailer-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smtp-mailer-api
  template:
    metadata:
      labels:
        app: smtp-mailer-api
    spec:
      containers:
      - name: smtp-mailer-api
        image: smtp-mailer-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: SMTP_HOST
          valueFrom:
            secretKeyRef:
              name: smtp-config
              key: host
        - name: SMTP_USERNAME
          valueFrom:
            secretKeyRef:
              name: smtp-config
              key: username
        - name: SMTP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: smtp-config
              key: password
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/detailed
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## 🔒 Seguridad

### Características de Seguridad Implementadas
- **Configuración por variables de entorno** - Credenciales nunca en código
- **Validación de entrada** con Pydantic para todos los endpoints
- **Rate limiting** configurable por IP y endpoint
- **Headers de seguridad** (CORS, CSP, HSTS)
- **Sanitización de datos** para prevenir inyecciones
- **Logging de seguridad** para auditoría de accesos

### Mejores Prácticas Recomendadas
- **Usar App Passwords** en lugar de contraseñas principales (Gmail)
- **Variables de entorno seguras** para credenciales SMTP
- **HTTPS obligatorio** en producción
- **Configurar CORS** apropiadamente para tu dominio
- **Monitorear logs** de seguridad regularmente
- **Rotar credenciales** periódicamente

### Configuración de Seguridad Avanzada

```bash
# Habilitar autenticación por API Key
API_KEY_ENABLED=true
API_KEY="tu-api-key-super-secreta"

# Configurar rate limiting estricto
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=50
MAX_REQUESTS_PER_HOUR=1000

# Configurar CORS específico
ALLOWED_ORIGINS="https://mi-app.com,https://admin.mi-app.com"
```

## 📊 Monitoreo y Observabilidad

### Health Checks

```bash
# Health check básico
curl http://localhost:8000/health

# Health check detallado (incluye conectividad SMTP)
curl http://localhost:8000/health/detailed
```

### Métricas Disponibles
- Tiempo de respuesta por endpoint
- Tasa de éxito/error de envío de correos
- Conectividad SMTP en tiempo real
- Estadísticas de rate limiting
- Uso de memoria y CPU

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
  "recipient": "user@example.com",
  "smtp_host": "smtp.gmail.com"
}
```

## 🧪 Testing

```bash
# Ejecutar tests unitarios
uv run pytest tests/ -v

# Ejecutar tests con coverage
uv run pytest tests/ --cov=app --cov-report=html

# Ejecutar tests de integración (requiere configuración SMTP)
uv run pytest tests/integration/ -v
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
- Usar type hints en todas las funciones

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

- **Issues:** [GitHub Issues](https://github.com/m4ck-y/SmtpMailer_FastAPI/issues)
- **Documentación:** [Wiki del Proyecto](https://github.com/m4ck-y/SmtpMailer_FastAPI/wiki)
- **Email:** soporte@tu-dominio.com

---

**SmtpMailer_FastAPI** - API stateless para envío de correos electrónicos con configuración por variables de entorno 🚀