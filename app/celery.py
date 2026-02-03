from celery import Celery
from app.config import settings

celeryApp = Celery(
    "app",
    broker = settings.redis_url,
    backend = settings.redis_url,
    include = ["app.tasks.cleanUnverifiedUsers"]
)

celeryApp.conf.beat_schedule = {
    "delete_unverified_users": {
        "task": "app.tasks.cleanUnverifiedUsers.delete_unverified_users",
        "schedule": settings.deleteUnverifiedUsersInterval # 3600 (1 hour) seconds, change to 86400 to start task every 24 hours or what interval you need, manually or in .env
    }
}