#Main py file for the AI-assisted-payment-registry
import logging

from config.settings import SHEET_ID
from services.email_reader import fetch_relevant_emails
from services.excel_updater import append_payment_record
from services.llm_parser import parse_with_llm
from services.notifier import send_confirmation_email
from services.pdf_parser import extract_text_from_email
from utils.parser import parse_payment_data

#Configuración del logger
logging.basicConfig(
    filename="agente.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
    )

#También hace logging en consola
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


if __name__ == "__main__":
    logging.info("Iniciando agente...")
    
    try:
        emails = fetch_relevant_emails()
        logging.info(f"Emails relevantes encontrados: {len(emails)}")
        
        if not emails:
            logging.info("No se encontraron emails nuevos que coincidan con los filtros")
        
        for i, mail in enumerate(emails, 1):
            msg = mail["raw"]
            extracted_text = extract_text_from_email(msg)

            logging.info(f"\n--- Email #{i} ---")
            logging.info(f"Asunto: {mail['subject']}")
            logging.info(f"De: {mail['from']}")
            logging.info(f"Fecha: {mail['date']}")           
            logging.info(f"Texto extraído:\n {extracted_text[:1000]}")  # muestra los primeros 1000 caracteres      


            parsed_data = parse_payment_data(extracted_text)

            if not parsed_data["monto"] or not parsed_data["fecha"] or not parsed_data["nombre"]:
                logging.info("Activando LLM por datos insuficientes...")
                parsed_data = parse_with_llm(extracted_text)


            if (
                not parsed_data["nombre"] 
                or parsed_data["nombre"].strip().lower() == parsed_data["destinatario"].strip().lower()
                ):
                parsed_data["nombre"] = mail['from']

            logging.info(f"Datos parseados: {parsed_data}")

            if parsed_data["monto"] and parsed_data["fecha"] and parsed_data["nombre"]:
                append_payment_record(SHEET_ID, parsed_data)
                logging.info("Registro guardado exitosamente")
                send_confirmation_email(
                    to_adress=mail['from'], 
                    original_subject=mail['subject'],
                    in_reply_to=msg["Message-ID"]
                    )
                
            else:
                logging.warning("Datos insuficientes para guardar el registro.")


            logging.info("="*50)    
    except Exception as e:
        logging.exception(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()