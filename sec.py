from django.core.management.utils import get_random_secret_key
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
with open('.env', 'w') as file:
    file.write(f'SECRET_KEY="{get_random_secret_key()}"\n')
    file.write(f'DEBUG=1\n')
    file.write(f'ALLOWED_HOSTS="{hostname} 127.0.0.1"')

