from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')

app = Celery('PROJECT')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule={
    'ovry10':{
        'task':'PROJECT.celery.pre',
        'schedule':20,
        # 'args':10
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True, ignore_result=False)
def pre(self):
    try:
        from cart.models import CartItem
        CartItem.objects.all().delete()
    except:
        print('not imported yet')
    return

