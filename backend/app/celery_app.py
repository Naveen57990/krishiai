from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "krishiai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_max_tasks_per_child=200,
    worker_concurrency=4,
)


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
