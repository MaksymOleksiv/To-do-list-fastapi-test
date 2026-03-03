import logging
import asyncio
from celery import Task
from app.core.celery_app import celery_app
from app.core.db import SessionLocal
from app.repositories.task import delete_expired_tasks
from app.services.email import send_email_task
from app.core.config import settings


logger = logging.getLogger(__name__)


async def verify_and_delete_expired():
    async with SessionLocal(expire_on_commit=False) as session:
        try:
            deleted_tasks = await delete_expired_tasks(session)

            if deleted_tasks:
                count = len(deleted_tasks)
                logger.info("Cleanup complete. Deleted %s tasks.", count)

                for task in deleted_tasks:
                    send_email_task.delay(
                        subject=f"⏰ Deadline missed: {task.title}",
                        email_to=settings.ADMIN_EMAIL,
                        body=f"<p>Task <b>{task.title}</b> was missed and has been automatically deleted by the system.</p>",
                    )
            else:
                logger.info("No expired tasks found.")
        except Exception as e:
            logger.error("Error during cleanup: %s", e)
            await session.rollback()


@celery_app.task(name="delete_expired_tasks_task")
def celery_delete_expired_tasks():
    logger.info("Starting background cleanup task...")

    asyncio.run(verify_and_delete_expired())


celery_app.conf.beat_schedule = {
    "delete-expired-every-minute": {
        "task": "delete_expired_tasks_task",
        "schedule": 60.0,
    }
}
