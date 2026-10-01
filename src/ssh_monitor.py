import os
import sys
import socket
from datetime import datetime
from notifier import send_telegram_message

def main():
    # PAM_TYPE indica la fase de autenticación. Solo nos interesa cuando se abre la sesión.
    pam_type = os.getenv("PAM_TYPE")
    if pam_type != "open_session":
        sys.exit(0)

    # Extraer datos inyectados por PAM
    pam_user = os.getenv("PAM_USER", "Desconocido")
    pam_rhost = os.getenv("PAM_RHOST", "IP Desconocida")
    
    hostname = socket.gethostname()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"🔐 *Inicio de Sesión SSH Exitoso*\n\n"
        f"*Servidor:* `{hostname}`\n"
        f"*Usuario:* `{pam_user}`\n"
        f"*IP Origen:* `{pam_rhost}`\n"
        f"*Fecha:* `{timestamp}`"
    )

    send_telegram_message(message)

if __name__ == "__main__":
    main()
