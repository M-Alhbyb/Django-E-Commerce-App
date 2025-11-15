import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce_app.settings')


app = Celery(
    'e_commerce_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
