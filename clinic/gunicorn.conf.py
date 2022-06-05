import multiprocessing

from clinic_app.config import FLASK_CONFIG

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
if FLASK_CONFIG == 'development':
    reload = True
