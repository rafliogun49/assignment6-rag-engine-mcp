from celery import Celery
from app.settings import settings

celery = Celery(
    "rag",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery.autodiscover_tasks(["app"])