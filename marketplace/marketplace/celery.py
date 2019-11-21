from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

app = Celery('marketplace')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'close-expired-auctions': {
#         'task': 'tasks.debug_task',
#         'schedule': crontab(minute=1),
#     },
# }


@app.task(bind=True)
def debug_task(self):
    with open('/tmp/wtf', 'w') as f:
        f.write('aaaaa')
        
    print('Request: {0!r}'.format(self.request))


