import os

from celery import Celery
from celery.schedules import crontab
from openwisp.utils import env_bool

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openwisp.settings')

app = Celery('openwisp',
             include=['openwisp.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

radius_schedule, topology_schedule = {}, {}

if env_bool(os.environ['SET_RADIUS_TASKS']):
    radius_schedule = {
        'radius-periodic-tasks': {
            'task': 'openwisp.tasks.radius_tasks',
            'schedule': crontab(minute=30, hour=3),
            'args': ()
        },
    }

if env_bool(os.environ['SET_TOPOLOGY_TASKS']):
    topology_schedule = {
        'topology-snapshot-tasks': {
            'task': 'openwisp.tasks.save_snapshot',
            'schedule': crontab(minute=45, hour=23),
            'args': ()
        },
        'topology-periodic-tasks': {
            'task': 'openwisp.tasks.update_topology',
            'schedule': crontab(minute='*/5'),
            'args': ()
        },
    }

app.conf.beat_schedule = {**radius_schedule, **topology_schedule}
