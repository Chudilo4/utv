from django.core.management.utils import get_random_secret_key
import socket
hostname = socket.gethostname()
with open('.env', 'w') as file:
    file.write(f'SECRET_KEY="{get_random_secret_key()}"\n'
               f'DEBUG=1\nALLOWED_HOSTS="{hostname} 127.0.0.1"')
