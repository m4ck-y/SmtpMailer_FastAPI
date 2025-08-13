# 📘 Documentación básica - `smtp-mailer-api`

### 🧩 Descripción general

**`smtp-mailer-api`** es una API simple y configurable para enviar correos electrónicos usando cualquier proveedor SMTP (como Gmail, Outlook, etc.).

Permite enviar correos comunes como códigos OTP, mensajes de bienvenida, recuperación de contraseña o emails personalizados.

La configuración requiere solo una clave SMTP válida y opcionalmente, plantillas HTML o contenido personalizado.

---

## 🔧 Configuración inicial

| URL | Método | Descripción |
| --- | --- | --- |
| `/smtp/configure` | POST | Configura las credenciales SMTP del servicio. Solo necesitas el host, puerto, usuario y clave SMTP. |
| `/smtp/status` | GET | Verifica que la configuración SMTP actual es válida y funcional (prueba de conexión). |

---

## 📤 Envío de correos

| URL | Método | Descripción |
| --- | --- | --- |
| `/emails/send` | POST | Enviar un correo genérico. El cuerpo puede incluir destinatario, asunto y contenido (texto o HTML). |
| `/emails/send-otp` | POST | Envía un correo con un código OTP a un usuario. El cuerpo debe incluir el email y el código. |
| `/emails/welcome` | POST | Envía un correo de bienvenida. Puede incluir nombre del usuario u otros datos para personalizar. |
| `/emails/recovery` | POST | Envía un enlace o código para recuperación de contraseña. |
| `/emails/custom` | POST | Permite enviar un correo personalizado usando una plantilla o HTML crudo. |

---

## 📚 Utilidades adicionales (opcional)

| URL | Método | Descripción |
| --- | --- | --- |
| `/emails/logs` | GET | Lista los correos enviados (si se activa el guardado de logs). |
| `/emails/logs/:id` | GET | Muestra el detalle de un correo enviado específico. |
| `/templates` | GET | Lista las plantillas predefinidas disponibles en el sistema. |
| `/templates/:type` | GET | Muestra una plantilla específica por tipo (ej. `welcome`, `otp`). |

---

## ✨ Características principales

| Funcionalidad | Descripción |
| --- | --- |
| 🔑 Configuración vía SMTP Key | Solo necesitas la configuración básica SMTP para empezar a usar el servicio. |
| 🧱 Endpoints separados y claros | Cada tipo de correo tiene su propio endpoint para facilitar la integración. |
| 🎨 Personalización | Permite usar plantillas o insertar HTML personalizado. |
| 🛠️ API RESTful | Pensada para ser simple de integrar con cualquier backend o frontend. |
| 🔒 Seguridad opcional | Puede integrar autenticación por token si se necesita proteger la API. |