import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Carga el .env de forma relativa al directorio del script
# Esto garantiza que funcione sin importar desde dónde lo llame PAM
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Error: Credenciales de Telegram no configuradas en .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # En scripts PAM, el output estándar a veces no es visible, 
        # pero evitará que el script falle silenciosamente a nivel de código.
        print(f"Error enviando notificación a Telegram: {e}")
