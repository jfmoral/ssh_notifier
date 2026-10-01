import sys
import re
import socket
import subprocess
from datetime import datetime
from notifier import send_telegram_message

def monitor_journal():
    # Comando para leer logs de SSH en tiempo real desde el final (-f)
    # Soporta 'ssh' (Debian/Ubuntu) y 'sshd' (RHEL/CentOS/Arch)
    cmd = ["journalctl", "-u", "ssh", "-u", "sshd", "-f", "-n", "0"]
    
    # Expresión regular para atrapar fallos de contraseña y usuarios inválidos
    # Ej: "Failed password for root from 192.168.1.50 port 22"
    # Ej: "Failed password for invalid user admin from 10.0.0.5 port 22"
    fail_regex = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+)")
    
    hostname = socket.gethostname()

    print(f"Iniciando monitoreo de fallos SSH en {hostname}...")

    try:
        # Iniciamos el subproceso para leer los logs en vivo
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            match = fail_regex.search(line)
            if match:
                user = match.group("user")
                ip = match.group("ip")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                message = (
                    f"⚠️ *Intento de Login SSH Fallido*\n\n"
                    f"*Servidor:* `{hostname}`\n"
                    f"*Usuario intentado:* `{user}`\n"
                    f"*IP Origen:* `{ip}`\n"
                    f"*Fecha:* `{timestamp}`"
                )
                
                send_telegram_message(message)
                
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    monitor_journal()
