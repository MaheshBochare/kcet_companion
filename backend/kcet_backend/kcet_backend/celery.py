
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kcet_backend.settings")

app = Celery("kcet_backend")

# 🔑 USE REDIS AS BROKER
app.conf.broker_url = "redis://kcet_redis:6379/0"
app.conf.result_backend = "redis://kcet_redis:6379/1"

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
