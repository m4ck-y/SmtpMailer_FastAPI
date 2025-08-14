from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


TEMPLATES_DIR = "app/templates"


from app.config import settings
from jinja2 import Environment, FileSystemLoader

class EmailOTPApplication:
    def __init__(self):
        print("Template dir", TEMPLATES_DIR)
        self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def Send_OTP(self, email: str, code: str, app_name: str):
        template = self.jinja_env.get_template("otp.html")

        context = {
            "email": email,
            "opt_code": code,
            "app_name": app_name
        }
        
        print("context: ",context)
        html_content = template.render(context)
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = 'Código de verificación'
        msg.attach(MIMEText(html_content, 'html'))
        # Enviar el correo
        print("SMPT_USE_SSL:", settings.SMTP_USE_SSL)
        print("SMPT_USE_TLS:", settings.SMTP_USE_TLS)
        print("SMTP_PORT:", settings.SMTP_PORT)
        
        if settings.SMTP_USE_SSL:
        # Método para puerto 465: Conexión segura desde el inicio
            print("Conectando con SMTP_SSL")
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(
            settings.SMTP_HOST, 
            settings.SMTP_PORT, 
            context=context,
            timeout=settings.SMTP_TIMEOUT
            )
        elif settings.SMTP_USE_TLS:
            # Método para puerto 587: Conexión normal que se actualiza a segura
            print("Conectando con SMTP")
            server = smtplib.SMTP(
                settings.SMTP_HOST, 
                settings.SMTP_PORT, 
                timeout=settings.SMTP_TIMEOUT
            )
            print("Starting starttsl")
            server.starttls()
        else:
            # Conexión no segura (no recomendada)
            print("Conectando sin seguridad..., SMTP")
            server = smtplib.SMTP(
                settings.SMTP_HOST, 
                settings.SMTP_PORT, 
                timeout=settings.SMTP_TIMEOUT
            )


            # El resto de tu lógica para iniciar sesión y enviar el correo
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        result = server.sendmail(settings.SMTP_FROM_NAME, email, msg.as_string())
        print("result:", result)
        if not result:
            print("Correo enviado exitosamente.")
        else:
            print("Fallo en el envío a:", result)
        server.quit()

            #logger.info(f"Correo enviado a {email}")