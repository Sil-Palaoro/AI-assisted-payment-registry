#Excel updater service
from services.drive_manager import get_sheet


def append_payment_record(sheet_id, data):
    row = [
        data["fecha"],
        data["monto"],
        data.get("nombre", ""),
        data["destinatario"],
        data.get("cvu_destino", "")
    ]
    sheet = get_sheet(sheet_id)
    sheet.append_row(row, value_input_option="USER_ENTERED")
