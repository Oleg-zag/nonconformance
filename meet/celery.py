from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meet.settings')
app = Celery('meet')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_currency': {
        'task': 'posts.tasks.currency_value',
        'schedule': crontab(minute='*/15'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight 
    },
#     'test': {
#         'task': 'celery.test',
#         'schedule': 10,  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight 
#     },
}
app.conf.timezone = 'UTC'
