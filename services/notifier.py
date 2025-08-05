#Notifier service for sending notifications to users
import smtplib
import ssl
from email.message import EmailMessage

from config.settings import APP_PASSWORD, EMAIL_USER


def send_confirmation_email(to_adress, original_subject, in_reply_to=None):
    try:
        subject = f"Re: {original_subject}"
        body = (
            "Recibido y registrado. Gracias!!\n\n"
            "Administración Mayéutica"
        )
        
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = to_adress
        msg.set_content(body)
        
        if in_reply_to:
            msg["In_Reply_To"] = in_reply_to
            msg["References"] = in_reply_to
        
        #Establecer conexión segura con el email server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, APP_PASSWORD)
            server.send_message(msg)
            
        print(f"Email de confirmación enviado a {to_adress}")
        
    except Exception as e:
        print(f"Error al enviar el email de confirmación a {to_adress}: {e}")