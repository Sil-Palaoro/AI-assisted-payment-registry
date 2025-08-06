#Settings file for the application
import os

from dotenv import load_dotenv

load_dotenv()  # carga variables del archivo .env

# Gmail
EMAIL_USER = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Google Drive / Sheets
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
SHEET_ID = os.getenv("SHEET_ID")

# Configuración general
IGNORED_SENDERS = os.getenv("IGNORED_SENDERS")

# Paths (ver si lo necesito más adelante)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DOWNLOAD_PATH = os.path.join(BASE_DIR, "data", "pdfs")

TESSERACT_CMD = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")

RECIPIENTS = [r.strip().lower() for r in os.getenv("RECIPIENTS", "").split(",") if r.strip()]
RECIPIENTS_ALIASES = [alias.strip().lower() for alias in os.getenv("RECIPIENTS_ALIASES", "").split(",")]
