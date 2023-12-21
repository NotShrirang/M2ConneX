from celery import Celery
from celery import shared_task
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumniportal.settings')

app = Celery('alumniportal', )
app = Celery('tasks', broker=settings.CELERY_BROKER_URL, backend='rpc://')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@shared_task
def debug_task(self):
    print("done")
