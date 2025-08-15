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

## 🐳 Despliegue con Docker

### Construcción y Ejecución

#### ⚠️ Importante: Consistencia de versiones Python

**Antes de construir**, verifica que las versiones de Python coincidan:

```bash
# Verificar versión en .python-version
cat .python-version
# Debe mostrar: 3.13

# Verificar versión en Dockerfile
grep "FROM python:" Dockerfile
# Debe mostrar: FROM python:3.13-bookworm
```

Si no coinciden, **actualiza el Dockerfile** para evitar tener 2 versiones de Python en la imagen:

```dockerfile
# ❌ INCORRECTO: Si .python-version = 3.13 pero usas:
FROM python:3.12-bookworm  # uv descargará Python 3.13 adicional

# ✅ CORRECTO: Versiones coincidentes
FROM python:3.13-bookworm  # Usa la misma versión que .python-version
```

#### 1. Construir la imagen Docker

```bash
# Construir la imagen con tag personalizado
docker build -t smtp-mailer-fastapi .
```

#### 2. Ejecutar el contenedor

**Opción 1: Usando archivo .env (recomendado):**

```bash
# Asegúrate de tener tu archivo .env configurado
docker run -p 8000:8000 --env-file .env smtp-mailer-fastapi
```

**Opción 2: Variables individuales:**

```bash
docker run -p 8000:8000 \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_USERNAME=tu-email@gmail.com \
  -e SMTP_PASSWORD=tu-app-password \
  smtp-mailer-fastapi
```

**Ejecutar en background:**

```bash
# Con archivo .env
docker run -d -p 8000:8000 --name smtp-mailer-api --env-file .env smtp-mailer-fastapi

# Con variables individuales
docker run -d -p 8000:8000 --name smtp-mailer-api \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_USERNAME=tu-email@gmail.com \
  -e SMTP_PASSWORD=tu-app-password \
  smtp-mailer-fastapi
```

### Variables de Entorno

#### 🔴 Obligatorias (sin defaults seguros)
```bash
SMTP_HOST=smtp.gmail.com          # Servidor SMTP
SMTP_USERNAME=tu-email@gmail.com  # Usuario SMTP
SMTP_PASSWORD=tu-app-password     # Contraseña SMTP
```

#### ✅ Opcionales (tienen defaults en Dockerfile)
```bash
DEBUG=false                       # Modo debug
ENVIRONMENT=production            # Entorno de ejecución
SMTP_PORT=587                     # Puerto SMTP (default: 587)
SMTP_USE_TLS=true                # Usar TLS (default: true)
SMTP_USE_SSL=false               # Usar SSL (default: false)
SMTP_TIMEOUT=30                  # Timeout SMTP (default: 30s)
SMTP_FROM_EMAIL=noreply@example.com  # Email remitente (default: noreply@example.com)
SMTP_FROM_NAME=SmtpMailer API        # Nombre remitente (default: SmtpMailer API)
ALLOWED_ORIGINS=*                # CORS origins (default: *)
```

### Comandos Útiles

```bash
# Ver logs del contenedor
docker logs smtp-mailer-api

# Ver logs en tiempo real
docker logs -f smtp-mailer-api

# Parar el contenedor
docker stop smtp-mailer-api

# Eliminar el contenedor
docker rm smtp-mailer-api

# Eliminar la imagen
docker rmi smtp-mailer-fastapi
```

### Verificación

Una vez ejecutándose, verifica que funciona:

```bash
# Health check
curl http://localhost:8000/health

# Documentación interactiva
open http://localhost:8000/docs
```

### 🔍 Optimización de Imagen Docker

#### Verificar tamaño de imagen
```bash
# Ver tamaño de la imagen construida
docker images smtp-mailer-fastapi

# Debería ser ~200-300MB con versiones coincidentes
# Si es >500MB, probablemente tienes versiones duplicadas de Python
```

#### Mejores prácticas
- **Mantén sincronizadas** las versiones de Python en `.python-version` y `Dockerfile`
- **Usa `--locked`** en `uv sync` para reproducibilidad exacta
- **Aprovecha el cache** de layers copiando `pyproject.toml` antes que el código
- **Verifica manualmente las versiones** antes de cada build para evitar duplicaciones

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