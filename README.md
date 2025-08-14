# 📧 SmtpMailer FastAPI

API RESTful stateless para envío de correos electrónicos con cualquier proveedor SMTP (Gmail, Outlook, SendGrid, etc.). Configuración simple por variables de entorno, sin base de datos.

## ✨ Características

- 🔧 **Configuración por variables de entorno** - Sin base de datos
- 📤 **Múltiples tipos de correo** - OTP, bienvenida, recuperación, personalizados
- 🎨 **Plantillas HTML** - Sistema de templates responsivos
- 🔒 **Seguridad integrada** - Rate limiting, validación, headers seguros
- ⚡ **Alta performance** - Operaciones asíncronas optimizadas
- 📊 **Monitoreo completo** - Logs estructurados y health checks

## 🚀 Stack Tecnológico

- **FastAPI 0.104+** - Framework web moderno
- **Python 3.12+** - Lenguaje base con type hints
- **Pydantic v2** - Validación automática de datos
- **aiosmtplib** - Cliente SMTP asíncrono

## 🔧 Instalación Rápida

```bash
# Instalar uv (gestor de paquetes Python moderno)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar y configurar el proyecto
git clone git@github.com:m4ck-y/SmtpMailer_FastAPI.git
cd SmtpMailer_FastAPI

# Instalar dependencias
uv sync

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales SMTP

# Ejecutar la aplicación
uv run uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000/docs

## ⚙️ Configuración SMTP

### Variables de Entorno

```bash
# Configuración SMTP (obligatorias)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=tu-email@gmail.com
SMTP_FROM_NAME="Mi Aplicación"

# Configuración básica
ENVIRONMENT=development
DEBUG=true
PORT=8000
```

### 📧 Configuración de Gmail (Paso a Paso)

Para usar Gmail como proveedor SMTP, necesitas crear una **Contraseña de Aplicación**. Sigue estos pasos:

#### 1. Activar Verificación en Dos Pasos

Ve a la configuración de seguridad de tu cuenta de Google: [myaccount.google.com/security](https://myaccount.google.com/security)

![Configuración de Seguridad](https://storage.googleapis.com/smtp_mailer/smtp_gmail_1.png)

Activa la **Verificación en dos pasos** si no la tienes habilitada. Es un requisito obligatorio para crear contraseñas de aplicación.

#### 2. Buscar Contraseñas de Aplicación

En la misma página de seguridad, busca "Contraseñas de aplicaciones" en el buscador:

![Buscar Contraseñas de Aplicación](https://storage.googleapis.com/smtp_mailer/smtp_gmail_2.png)

O ve directamente a: [myaccount.google.com/apppasswords](https://myaccount.google.com/u/1/apppasswords)

#### 3. Crear Nueva Contraseña

![Crear Contraseña de Aplicación](https://storage.googleapis.com/smtp_mailer/smtp_gmail_3.png)

1. Selecciona "Otra (nombre personalizado)"
2. Dale un nombre descriptivo como "SmtpMailer API"
3. Haz clic en "Generar"
4. **Copia la contraseña de 16 caracteres** - esta será tu `SMTP_PASSWORD`

#### 4. Configuración Final

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # La contraseña de 16 caracteres generada
SMTP_USE_TLS=true
```

> **⚠️ Importante:** Guarda la contraseña de aplicación inmediatamente. Una vez que cierres la ventana, no podrás volver a verla.

#### 📸 Evidencia de Configuración

Las capturas de pantalla de este tutorial están almacenadas en Google Cloud Storage:

![Bucket Cloud Storage](https://storage.googleapis.com/smtp_mailer/smt_mailer_bucket.png)

![Permisos del Bucket](https://storage.googleapis.com/smtp_mailer/smt_mailer_bucket_permissions.png)

**Referencias oficiales:**
- [Configurar cliente de correo con Gmail](https://support.google.com/mail/answer/7126229)
- [Enviar correo desde aplicaciones](https://support.google.com/a/answer/176600?hl=es)

### 🔧 Otros Proveedores SMTP

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

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check del servicio |
| `/smtp/status` | GET | Verificar configuración SMTP |
| `/emails/send-otp` | POST | Enviar código OTP |
| `/emails/welcome` | POST | Enviar correo de bienvenida |
| `/emails/send` | POST | Enviar correo personalizado |

### Ejemplo de Uso

```bash
# Verificar estado del servicio
curl http://localhost:8000/health

# Enviar código OTP
curl -X POST "http://localhost:8000/emails/send-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "usuario@ejemplo.com",
    "otp_code": "123456",
    "user_name": "Juan Pérez"
  }'
```

**Documentación completa:** http://localhost:8000/docs

## 🚀 Despliegue con Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Instalar uv y dependencias
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copiar código fuente
COPY . .
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  smtp-mailer-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_USERNAME=tu-email@gmail.com
      - SMTP_PASSWORD=tu-app-password
      - SMTP_USE_TLS=true
    restart: unless-stopped
```

## 📚 Documentación

Una vez ejecutándose, la documentación interactiva estará disponible en:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

**SmtpMailer FastAPI** - API stateless para envío de correos electrónicos 🚀