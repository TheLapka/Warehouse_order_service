import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_mining.settings")

app = Celery("order_in_cel")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.timezone = "UTC"
