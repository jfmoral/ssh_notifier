# 🛡️ SSH Telegram Notifier

Un sistema de monitoreo ligero, modular y seguro escrito en Python que envía notificaciones en tiempo real a Telegram sobre la actividad de acceso SSH en tu servidor.

Detecta y notifica dos eventos críticos:
1. **Inicios de sesión exitosos:** Utilizando la integración nativa con PAM (Pluggable Authentication Modules).
2. **Intentos de inicio de sesión fallidos:** Leyendo los logs del sistema (`journalctl`) en tiempo real para evitar bloqueos del servicio SSH.

---

## 🏗️ Arquitectura de Seguridad

Este proyecto fue diseñado teniendo la ciberseguridad y la disponibilidad como prioridades:
* **Desacoplamiento Crítico:** Los fallos de autenticación se monitorean pasivamente vía logs. Nunca se usa PAM para bloquear accesos fallidos, previniendo que un error en el script o la caída de la API de Telegram bloqueen el acceso legítimo al servidor (Denegación de Servicio accidental).
* **Ejecución Aislada:** Utiliza un entorno virtual (`venv`) de Python, evitando conflictos con las dependencias del sistema operativo base.
* **Manejo de Secretos:** Los tokens se gestionan a través de un archivo `.env` restringido, el cual está excluido del control de versiones (`.gitignore`).

---

## 📋 Requisitos Previos

* Sistema Operativo Linux con `systemd` y `journalctl` (Debian, Ubuntu, Arch, RHEL, etc.).
* Python 3 y el módulo `venv` instalado (`sudo apt install python3-venv` en Debian/Ubuntu).
* Un Bot de Telegram (creado vía [@BotFather](https://t.me/BotFather)) y tu Chat ID.

---

## 🚀 Instalación y Configuración Base

**1. Clonar el repositorio**
Recomendamos instalar la herramienta en `/opt/` para mantener el sistema organizado.
```bash
sudo git clone https://github.com/TU_USUARIO/ssh_notifier.git /opt/ssh_notifier
sudo chown -R $USER:$USER /opt/ssh_notifier
cd /opt/ssh_notifier
```

**2. Crear el entorno virtual e instalar dependencias**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**3. Configurar las credenciales**
Copia el archivo de ejemplo y configura tu Token y Chat ID.
```bash
cp .env.example .env
nano .env
```
*Asegura el archivo para que solo el propietario (root/admin) pueda leerlo:*
```bash
chmod 600 .env
```

**4. Dar permisos de ejecución a los scripts**
```bash
chmod +x src/ssh_monitor.py src/fail_monitor.py
```

---

## ⚙️ Configuración Módulo 1: Accesos Exitosos (PAM)

Este módulo inyecta el script en el proceso de inicio de sesión de Linux.

**1. Editar el archivo PAM de SSH:**
```bash
sudo nano /etc/pam.d/sshd
```

**2. Agregar la ejecución del script al final del archivo:**
Añade la siguiente línea. El parámetro `optional` es vital para garantizar que puedas entrar al servidor incluso si el script falla.
```text
session optional pam_exec.so /opt/ssh_notifier/venv/bin/python /opt/ssh_notifier/src/ssh_monitor.py
```
*(Guarda y cierra el archivo. No es necesario reiniciar el servicio SSH).*

---

## ⚙️ Configuración Módulo 2: Accesos Fallidos (Systemd)

Este módulo corre como un servicio en segundo plano monitoreando intentos fallidos de contraseñas o usuarios inválidos.

**1. Crear el archivo de servicio:**
```bash
sudo nano /etc/systemd/system/ssh-fail-notifier.service
```

**2. Pegar la siguiente configuración:**
```ini
[Unit]
Description=SSH Failed Login Notifier (Telegram)
After=network.target

[Service]
Type=simple
ExecStart=/opt/ssh_notifier/venv/bin/python /opt/ssh_notifier/src/fail_monitor.py
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
```

**3. Habilitar e iniciar el servicio:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ssh-fail-notifier.service
sudo systemctl start ssh-fail-notifier.service
```

---

## 🧪 Pruebas de Validación

### Validar Accesos Exitosos
1. Mantén tu sesión SSH actual abierta (por seguridad).
2. Abre una nueva terminal y conéctate al servidor vía SSH.
3. Deberás recibir un mensaje en Telegram con el título **🔐 Inicio de Sesión SSH Exitoso**, mostrando tu IP y el usuario.

### Validar Accesos Fallidos
1. Desde cualquier terminal fuera del servidor, intenta conectarte usando un usuario que no exista o una contraseña incorrecta:
   ```bash
   ssh root_falso@<IP_DEL_SERVIDOR>
   ```
2. Al ingresar una contraseña errónea, el servicio detectará el log y recibirás una alerta en Telegram con el título **⚠️ Intento de Login SSH Fallido**.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo, modificarlo y distribuirlo, tanto para uso personal como comercial.
