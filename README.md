# AI-assisted-payment-registry

🎯 Un asistente automatizado que procesa comprobantes de pago enviados por email, extrae los datos relevantes (monto, fecha, pagador, destinatario y medio de pago) desde archivos adjuntos o imágenes embebidas, y los registra en una planilla de Google Drive. Además, responde automáticamente al remitente confirmando la recepción del pago.

## 📌 Funcionalidades principales

- 🔍 Lee correos electrónicos entrantes desde una cuenta de Gmail configurada.
- 📎 Extrae texto desde PDFs e imágenes (OCR).
- 🤖 Usa IA (Claude API de Anthropic) para interpretar comprobantes con formatos diversos.
- 📊 Registra los datos extraídos en un archivo de Excel en Google Drive.
- 📧 Envía respuestas automáticas por email, confirmando el registro del pago.
- 🧠 Si no se encuentra el nombre del pagador, se toma como fallback el correo del remitente.

## 🛠️ Tecnologías utilizadas

- Python 3.12+
- `imaplib`, `email`, `logging` (estándar)
- `pdfplumber`, `pytesseract`, `Pillow` para extracción de texto
- `anthropic` para integración con Claude AI
- `google-api-python-client` para actualizar Google Sheets
- `smtplib` para enviar emails
- SQLite opcional para logging de registros

## 🧱 Estructura del proyecto

```bash
AI-assisted-payment-registry/
├── main.py
├── config/
│ └── settings.py
├── services/
│ ├── email_reader.py
│ ├── pdf_parser.py
│ ├── drive_manager.py
│ ├── excel_updater.py
│ └── notifier.py
├── utils/
│ ├── parser.py
│ └── helpers.py
├── data/
│ └── pagos.db
├── logs/
│ └── agent.log
├── requirements.txt
└── README.md
```

## ⚙️ Configuración

1. **Clona este repositorio**:

```bash
git clone https://github.com/tu-usuario/AI-assisted-payment-registry.git
cd AI-assisted-payment-registry
```

2. **Crea un entorno virtual e instala las dependencias**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```


3. **Configura las credenciales y variables necesarias:**


- Edita el archivo config/settings.py con tus datos guardados en el .env:

- Datos de Gmail (email y contraseña de aplicación)

- API Key de Anthropic (Claude)

- ID de tu Google Sheet de Drive



También asegúrate de tener instalado:


- Tesseract OCR (recomendado vía instalador si usás Windows)

- Credenciales de Google habilitadas (token y client_secret para Google Sheets)


4. **Ejecuta el agente:**


```bash
python main.py
```


## 🧠 **Cómo funciona**

1. Lee los emails no leídos y filtra los que contienen comprobantes de pago.
2. Extrae texto desde los adjuntos (PDF o imagen) o el cuerpo del mensaje.
3. Intenta parsear los datos directamente.
4. Si no logra extraer toda la información, recurre al modelo Claude de Anthropic para interpretarlos con IA.
5. Registra los datos en Google Sheets.
6. Responde automáticamente al remitente confirmando la operación.


📦 Dependencias
Están detalladas en requirements.txt. Podés generarlo nuevamente con:

```bash
pip freeze > requirements.txt

```


## 📝 Licencia

Este proyecto está licenciado bajo los términos de la [Licencia MIT](LICENSE).


## 🤝 Contribuciones
¡Contribuciones, mejoras o ideas son bienvenidas! Podés hacer un fork del repositorio y enviar un Pull Request, o abrir un Issue si encontrás algún problema.


## 📬 Contacto

Silvina Palaoro

📧 silvinapalaoro@gmail.com

🌐 https://sil-palaoro-sdyw.vercel.app/

🌐 https://www.linkedin.com/in/silvina-palaoro/
