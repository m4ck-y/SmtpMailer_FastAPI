import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from app.config import settings
from app.waitlist.models import WaitlistEmailRequest, WaitlistEmailResponse


class EmailWaitlistApplication:
    """
    Controlador de aplicación para envío de emails de confirmación de waitlist.
    
    Implementa la lógica de negocio para el envío de correos de confirmación
    cuando un usuario se registra en la lista de espera. Utiliza plantillas HTML
    responsivas y configuración automática desde variables de entorno.
    """
    
    def __init__(self):
        """Inicializa el controlador con configuración de templates."""
        # Configurar Jinja2 para templates
        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        
        print(f"[INFO] EmailWaitlistApplication inicializado")
        print(f"[INFO] Template directory: {template_dir}")
    
    def send_waitlist_email(self, request: WaitlistEmailRequest) -> WaitlistEmailResponse:
        """
        Envía email de confirmación de registro en waitlist con personalización de ofertas.
        
        Procesa la solicitud de envío de email de confirmación utilizando
        la plantilla HTML responsiva y lógica condicional basada en las ofertas
        especificadas por el usuario.
        
        Args:
            request (WaitlistEmailRequest): **Datos del email** con información
                                          del usuario, ofertas y configuración opcional.
        
        Returns:
            WaitlistEmailResponse: **Resultado del envío** con detalles completos,
                                  tipo de mensaje y metadatos para debugging.
        
        Example:
            >>> controller = EmailWaitlistApplication()
            >>> request = WaitlistEmailRequest(
            ...     email="usuario@ejemplo.com",
            ...     user_name="Juan Pérez",
            ...     offerings=["CRM Avanzado", "Analytics Pro"]
            ... )
            >>> response = controller.send_waitlist_email(request)
            >>> response.success
            True
            >>> response.message_type
            'multiple'
        """
        try:
            print(f"[INFO] Iniciando envío de email de waitlist a: {request.email}")
            print(f"[INFO] Ofertas especificadas: {request.offerings}")
            
            # Preparar datos básicos para la plantilla
            user_name = request.user_name or "Usuario"
            website_url = request.website_url or settings.WEBSITE_URL
            show_website_button = bool(website_url and website_url.strip())
            
            # Generar texto personalizado según las ofertas
            offerings_data = self._generate_offerings_text(request.offerings)
            
            template_data = {
                "app_name": settings.APP_NAME,
                "company_name": settings.COMPANY_NAME,
                "logo_url": settings.COMPANY_LOGO_URL,
                "support_email": settings.SUPPORT_EMAIL,
                "website_url": website_url,
                "user_name": user_name,
                "user_email": request.email,
                "show_website_button": show_website_button,
                **offerings_data  # Incluir datos de ofertas
            }
            
            print(f"[INFO] Datos de plantilla preparados para: {user_name}")
            print(f"[INFO] Tipo de mensaje: {offerings_data['message_type']}")
            
            # Renderizar plantilla HTML
            template = self.jinja_env.get_template("waitlist.html")
            html_content = template.render(**template_data)
            
            print(f"[INFO] Plantilla HTML renderizada exitosamente")
            
            # Crear mensaje de email
            message = MIMEMultipart("alternative")
            message["Subject"] = f"¡Gracias por registrarte! - {settings.APP_NAME}"
            message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            message["To"] = request.email
            
            # Crear versión de texto plano como fallback
            text_content = self._generate_text_content(
                user_name, request.email, website_url, show_website_button, offerings_data
            )
            
            # Adjuntar ambas versiones
            part1 = MIMEText(text_content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")
            
            message.attach(part1)
            message.attach(part2)
            
            print(f"[INFO] Mensaje de email preparado")
            
            # Enviar email
            self._send_email_smtp(message, request.email)
            
            # Crear respuesta exitosa
            response = WaitlistEmailResponse(
                success=True,
                message="Email de confirmación de waitlist enviado exitosamente",
                email_sent_to=request.email,
                timestamp=datetime.utcnow().isoformat() + "Z",
                user_name=user_name,
                has_website_button=show_website_button,
                logo_used=settings.COMPANY_LOGO_URL,
                offerings_count=len(request.offerings),
                message_type=offerings_data['message_type'],
                offerings_text=offerings_data['offerings_text'],
                offerings_text_html=offerings_data['offerings_text_html']
            )
            
            print(f"[INFO] Email de waitlist enviado exitosamente a: {request.email}")
            return response
            
        except Exception as e:
            error_msg = f"Error enviando email de waitlist: {str(e)}"
            print(f"[ERROR] {error_msg}")
            
            # Generar datos de ofertas para respuesta de error
            offerings_data = self._generate_offerings_text(request.offerings)
            
            # Crear respuesta de error
            return WaitlistEmailResponse(
                success=False,
                message=error_msg,
                email_sent_to=request.email,
                timestamp=datetime.utcnow().isoformat() + "Z",
                user_name=request.user_name or "Usuario",
                has_website_button=bool(request.website_url),
                logo_used=settings.COMPANY_LOGO_URL,
                offerings_count=len(request.offerings),
                message_type=offerings_data['message_type'],
                offerings_text=offerings_data['offerings_text'],
                offerings_text_html=offerings_data['offerings_text_html']
            )
    
    def _generate_offerings_text(self, offerings: list[str]) -> dict:
        """
        Genera el texto personalizado según las ofertas especificadas.
        
        Implementa la lógica condicional para diferentes casos:
        - Sin ofertas: mensaje genérico de plataforma
        - Una oferta: mensaje singular personalizado
        - Múltiples ofertas: mensaje plural con lista en negrita
        
        Args:
            offerings (list[str]): **Lista de ofertas** especificadas por el usuario.
        
        Returns:
            dict: **Datos de ofertas** con texto personalizado y tipo de mensaje.
                 Incluye: offerings_text, offerings_text_html, message_type, availability_message
        
        Example:
            >>> self._generate_offerings_text(["CRM", "Analytics"])
            {
                'offerings_text': 'CRM, Analytics',
                'offerings_text_html': '<strong>CRM</strong>, <strong>Analytics</strong>',
                'message_type': 'multiple',
                'availability_message': 'En cuanto nuestras soluciones CRM, Analytics estén disponibles oficialmente'
            }
        """
        offerings_count = len(offerings)
        
        if offerings_count == 0:
            # Sin ofertas específicas - mensaje genérico de plataforma
            return {
                'offerings_text': 'nuestra plataforma',
                'offerings_text_html': 'nuestra plataforma',
                'message_type': 'platform',
                'availability_message': 'En cuanto nuestra plataforma esté disponible oficialmente'
            }
        elif offerings_count == 1:
            # Una sola oferta - mensaje singular
            offering_name = offerings[0]
            return {
                'offerings_text': offering_name,
                'offerings_text_html': f'<strong>{offering_name}</strong>',
                'message_type': 'single',
                'availability_message': f'En cuanto <strong>{offering_name}</strong> esté disponible oficialmente'
            }
        else:
            # Múltiples ofertas - mensaje plural con lista en negrita
            offerings_text = ', '.join(offerings)
            offerings_text_html = ', '.join([f'<strong>{offering}</strong>' for offering in offerings])
            return {
                'offerings_text': offerings_text,
                'offerings_text_html': offerings_text_html,
                'message_type': 'multiple',
                'availability_message': f'En cuanto nuestras soluciones {offerings_text_html} estén disponibles oficialmente'
            }
    
    def _generate_text_content(self, user_name: str, user_email: str, website_url: str, 
                              show_website_button: bool, offerings_data: dict) -> str:
        """
        Genera el contenido de texto plano personalizado para el email.
        
        Crea la versión de texto plano del email utilizando los datos de ofertas
        y la información del usuario para mantener consistencia con la versión HTML.
        
        Args:
            user_name (str): **Nombre del usuario** para personalización.
            user_email (str): **Email del usuario** para confirmación.
            website_url (str): **URL del sitio web** para incluir si está disponible.
            show_website_button (bool): **Indica si mostrar URL** en el texto.
            offerings_data (dict): **Datos de ofertas** generados por _generate_offerings_text.
        
        Returns:
            str: **Contenido de texto plano** personalizado para el email.
        """
        return f"""
¡Gracias por unirte a {settings.APP_NAME}!

Hola {user_name},

Hemos registrado exitosamente tu correo ({user_email}) en nuestra lista de notificaciones.

{offerings_data['availability_message']}, te enviaremos un correo para que puedas acceder al sistema y disfrutar todas sus funcionalidades.

¿Tienes alguna pregunta?
Puedes escribirnos a {settings.SUPPORT_EMAIL} si necesitas más información sobre el proyecto o el proceso de lanzamiento.

{website_url if show_website_button else ''}

© 2025 {settings.COMPANY_NAME}. Todos los derechos reservados.
Este es un mensaje automático, no respondas directamente.
        """.strip()

    def _send_email_smtp(self, message: MIMEMultipart, recipient_email: str) -> None:
        """
        Envía el email usando configuración SMTP.
        
        Método privado que maneja la conexión SMTP y el envío real del mensaje
        utilizando la configuración de variables de entorno.
        
        Args:
            message (MIMEMultipart): **Mensaje preparado** para envío.
            recipient_email (str): **Email del destinatario** para logging.
        
        Raises:
            Exception: Si falla la conexión SMTP o el envío del mensaje.
        """
        try:
            print(f"[INFO] Conectando a servidor SMTP: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
            
            # Crear contexto SSL
            context = ssl.create_default_context()
            
            # Conectar al servidor SMTP
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls(context=context)
                    print(f"[INFO] TLS habilitado")
                
                # Autenticarse
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                print(f"[INFO] Autenticación SMTP exitosa")
                
                # Enviar mensaje
                server.send_message(message)
                print(f"[INFO] Mensaje enviado exitosamente via SMTP a: {recipient_email}")
                
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Error de autenticación SMTP: {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise Exception(error_msg)
            
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"Destinatario rechazado por servidor SMTP: {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise Exception(error_msg)
            
        except smtplib.SMTPException as e:
            error_msg = f"Error SMTP: {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise Exception(error_msg)