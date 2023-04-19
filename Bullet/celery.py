import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsboard.settings')
app = Celery('newsboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check_new_post_every_30_sec': {
        'task': 'app1.tasks.celery_notify_about_new_post',
        'schedule': 30.0,
        'args': None
        }
}

app.autodiscover_tasks()