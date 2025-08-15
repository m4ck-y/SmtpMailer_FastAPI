# 🐳 Dockerfile - SmtpMailer FastAPI
# Imagen optimizada para producción con uv como gestor de paquetes

# ⚠️ CRÍTICO: Esta versión DEBE coincidir con .python-version
# Si no coincide, uv descargará otra versión de Python, duplicando el tamaño de la imagen
# .python-version = 3.13 → FROM python:3.13-bookworm
FROM python:3.13-bookworm

# Copiar uv (gestor de paquetes Python ultrarrápido) desde imagen oficial
COPY --from=ghcr.io/astral-sh/uv:0.8.8 /uv /uvx /bin/

# Establecer directorio de trabajo
WORKDIR /app

# === OPTIMIZACIÓN DE CACHE DE LAYERS ===
# Copiar archivos de configuración primero para aprovechar cache de Docker
# Si pyproject.toml/uv.lock no cambian, esta layer se reutiliza
COPY pyproject.toml uv.lock ./

# Instalar dependencias usando uv (mucho más rápido que pip)
# --locked: usa exactamente las versiones del uv.lock
RUN uv sync --locked

# Copiar código fuente después de instalar dependencias
# Esto permite que cambios en el código no invaliden el cache de dependencias
COPY . .

# === VARIABLES DE ENTORNO POR DEFECTO ===
# Estas pueden ser sobrescritas al ejecutar el contenedor
# Solo incluimos valores seguros y no sensibles

# Configuración de la aplicación
ENV DEBUG=false
ENV ENVIRONMENT=production

# Configuración SMTP (valores estándar)
ENV SMTP_PORT=587
ENV SMTP_USE_TLS=true
ENV SMTP_USE_SSL=false
ENV SMTP_TIMEOUT=30
# Variables SMTP con valores por defecto
ENV SMTP_FROM_EMAIL=noreply@example.com
# ⚠️ IMPORTANTE: Valores con espacios DEBEN ir entre comillas en Docker
# Sin comillas: ENV NAME=Mi App → Error "can't find = in App"
# Con comillas: ENV NAME="Mi App" → Correcto
ENV SMTP_FROM_NAME="SmtpMailer API"

# Configuración CORS (permisiva por defecto)
# NOTA: El asterisco (*) no necesita comillas en Docker ENV
ENV ALLOWED_ORIGINS=*
# Listas separadas por comas tampoco necesitan comillas si no hay espacios
ENV ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ENV ALLOWED_HEADERS=*

# NOTA: Variables sensibles como SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD
# NO se incluyen aquí por seguridad. Deben pasarse al ejecutar el contenedor.

# Exponer puerto 8000 para la aplicación FastAPI
EXPOSE 8000

# Comando de ejecución optimizado para producción
# --host 0.0.0.0: permite conexiones desde fuera del contenedor
# --port 8000: puerto estándar para APIs
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
