#Drive manager service for managing Google Drive files and folders.
import gspread
from google.oauth2.service_account import Credentials

from config.settings import CREDENTIALS_FILE


def get_sheet(sheet_id):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    return sheet.sheet1 # Return the first sheet of the spreadsheet