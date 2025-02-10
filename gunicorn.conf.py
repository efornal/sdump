# gunicorn.conf.py
import os
import multiprocessing

# Leer las variables de entorno
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')  # Valor por defecto: 0.0.0.0:8000
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))  # Valor por defecto: CPU count * 2 + 1
threads = int(os.getenv('GUNICORN_THREADS', 2))  # Valor por defecto: 2
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))  # Valor por defecto: 120 segundos
loglevel = os.getenv('GUNICORN_LOGLEVEL', 'info')  # Valor por defecto: info

# Logs
accesslog = os.getenv('GUNICORN_ACCESSLOG', '-')  # Logs en consola por defecto
errorlog = os.getenv('GUNICORN_ERRORLOG', '-')    # Logs de error en consola por defecto
