#Email reader service import imaplib
import email
import imaplib
import re
from datetime import datetime, timedelta
from email.header import decode_header

from config.settings import APP_PASSWORD, EMAIL_USER, IGNORED_SENDERS

# Configuración de Gmail IMAP

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = EMAIL_USER  
APP_PASSWORD = APP_PASSWORD  #Contraseña de aplicación
SUBJECT_KEYWORDS = ["comprobante", "Re: Aviso de pago", "transferencia", "pago", "cuota", "matricula"]
FOLDER = "inbox"
DAYS_LIMIT = 60  # Días atrás para buscar correos relevantes
IGNORED_SENDERS = IGNORED_SENDERS   #TODO agregar email de verdadero en .env cuando lo implementemos

# Función auxiliar


def email_has_attachment_or_inline_image(msg):
    """Verifica si el mensaje tiene al menos un archivo adjunto o una imagen embebida."""
    for part in msg.walk():
        content_disposition = part.get("Content-Disposition", "")
        content_type = part.get_content_type()

        # Archivos adjuntos tradicionales
        if "attachment" in content_disposition.lower():
            return True

        # Imágenes embebidas en el cuerpo (por ejemplo, pegadas)
        if "inline" in content_disposition.lower() and content_type.startswith("image/"):
            return True

    return False

# Función ppal

def fetch_relevant_emails():
    # Conexión segura a Gmail IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select(FOLDER)

    # Obtener la fecha límite (hoy - 15 días)
    date_limit = (datetime.now() - timedelta(days=DAYS_LIMIT)).strftime("%d-%b-%Y")

    # Buscar correos desde esa fecha
    status, messages = mail.search(None, f'(SINCE "{date_limit}")')
    email_ids = messages[0].split()    
    if not email_ids:
        print("No se encontraron correos relevantes.")
        mail.logout()
        return []
    
    matched_emails = []

    
    for email_id in reversed(email_ids):  # Procesamos del más reciente al más viejo        
            status, data = mail.fetch(email_id, "(BODY.PEEK[])")
            msg = email.message_from_bytes(data[0][1])
                       

            # Obtener y decodificar el asunto
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
            subject_lower = subject.lower()

            try:
                # Filtrar por palabras clave y adjunto
                if any(keywords in subject_lower for keywords in SUBJECT_KEYWORDS)and email_has_attachment_or_inline_image(msg):
                    from_address = msg["From"]
                    # Verificar si el remitente está en la lista de ignorados, y asegurarme que sea un fullmatch no solo un match parcial
                    if any(re.fullmatch(re.escape(sender), from_address.strip()) for sender in IGNORED_SENDERS):
                        print(f"Email ID {email_id} ignorado por remitente: {from_address}")
                        continue  # salteamos este mensaje

                    matched_emails.append({
                        "id": email_id,
                        "subject": subject,
                        "from": msg["From"],
                        "date": msg["Date"],
                        "raw": msg,
                    })                    
                    mail.store(email_id, 'FLAGS', '\\Seen')
            except Exception as e: 
                print(f"Error al procesar email ID {email_id.decode(errors='ignore')}: {e}")
    
    mail.logout()
    return matched_emails
