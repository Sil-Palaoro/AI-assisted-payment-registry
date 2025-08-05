#Función para parsear la información extraida de los emails de pago
import re

from dateutil import parser as dateparser


def parse_payment_data(text):
    """Extrae monto, fecha, nombre de pagador, y nombre de destinatario y cvu del texto de un comprobante"""
    data = {
        "monto": None,
        "fecha": None,
        "nombre": None,
        "destinatario": None, 
        "cvu_destino": None
    }
    
    #Monto (en pesos o dólares)
    monto_match = re.search(
        r"\$ ?([\d\.,]+)"
        r"|([\d\.,]+)\s*(USD|EUR|ARS)?"
        r"|(USD|EUR|ARS)?\s*([\d\.,]+)",
        text,
        re.IGNORECASE
        )
    if monto_match:        
        try:
            # raw = monto_match.group(1) or monto_match.group(2)
            raw = next(g for g in monto_match.groups() if g and re.match(r"[\d\.,]+", g))
            monto = raw.replace(".", "").replace(",", ".")
            data["monto"] = "{:.2f}".format(float(monto))
        except Exception: 
            pass
        
    #Fecha (distintos formatos) 
    date_match = re.search(
        r"(\d{1,2}/\d{1,2}/\d{4})"                                # formato 03/02/2025
        r"|(\d{1,2} de [a-zA-Z]+ de \d{4})"                        # 17 de febrero de 2025
        r"|([a-zA-Z]+ \d{1,2}, \d{4})"                             # enero 07, 2025 o February 7, 2025
        r"|([a-zA-Z]+, \d{1,2} de [a-zA-Z]+ de \d{4})",            # Lunes, 17 de febrero de 2025 
        text,
        re.IGNORECASE
        )
    if date_match:
        try:
            raw_fecha = date_match.group(0)
            parsed = dateparser.parse(raw_fecha, dayfirst=True)
            data["fecha"] = parsed.strftime("%Y-%m-%d")
        except Exception:
            pass
        
    #Nombre del pagador
    de_match = re.search(r"De[: ]+?\s*([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.]+)", text) \
    or re.search(r"pagada por\s*([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.]+)", text)
    if de_match:
        data["nombre"] = de_match.group(1).strip()
    
    
    #Destinatario
    para_match = re.search(r"(o\s+)Para[\s:\n]+([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.]+)", text, re.IGNORECASE) 
        # or re.search(r"Enviado a\s*([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.]+)", text) \
        #     or re.search(r"Titular Destino\s*([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.]+)", text) \
        #         or re.search(r"Destino\s*([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.]+)", text)
    if para_match:
        data["destinatario"] = para_match.group(2).strip()
        
    
    #CVU o CBU destino
    cvu_match = re.search(r"(CBU|CVU)[: ]+(\d{16,22})", text)
    if cvu_match:
        data["cvu_destino"] = cvu_match.group(2)
        
    return data

