from celery import Celery
from app.core.config import settings

celery_app = Celery(
    'device_monitor',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
    backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1',
    include=['app.tasks.stats']
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
)
