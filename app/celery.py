import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'crypto': {
        'task': 'crypto.tasks.binance_price',
        'schedule': 30.0,  # Run every 30 seconds
    },
}

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()