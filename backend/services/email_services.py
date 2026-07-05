import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import SecretStr, NameEmail


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD = SecretStr(os.getenv("MAIL_PASSWORD", "")),
    MAIL_FROM = os.getenv("MAIL_FROM", ""),
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

# Instanciamos el motor de correos
motor_correos = FastMail(conf)

# LA FUNCIÓN QUE HACE EL TRABAJO
async def enviar_correo_real(email_destinatario: str, nombre_destinatario: str, asunto: str, cuerpo_html: str):
    
    contacto_formateado = NameEmail(nombre_destinatario, email_destinatario)
    
    mensaje = MessageSchema(
        subject=asunto,
        recipients=[contacto_formateado],
        body=cuerpo_html,
        subtype=MessageType.html
    )
    
    try:
        await motor_correos.send_message(mensaje)
        print(f"Correo enviado con éxito a {contacto_formateado}")
    except Exception as e:
        print(f"Error al enviar correo a {contacto_formateado}: {str(e)}")