import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE","allsafe_website_info.settings")

app=Celery("allsafe_website_info")

app.config_from_object(settings,namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_tasks(self):
    print(f'Request: {self.request!r}')
