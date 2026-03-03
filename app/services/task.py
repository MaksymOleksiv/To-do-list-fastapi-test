from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    get_task_history,
)
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate, TaskHistoryResponse
from app.core.config import StatusEnum
from app.services.email import send_email_task
from app.core.config import settings


async def get_tasks(
    db_session: AsyncSession,
    status: StatusEnum | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[TaskResponse]:
    return [
        TaskResponse.model_validate(task)
        for task in await get_all_tasks(db_session, status, skip, limit)
    ]


async def get_task(db_session: AsyncSession, task_id: int) -> TaskResponse:
    if task := await get_task_by_id(db_session, task_id):
        return TaskResponse.model_validate(task)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


async def create_new_task(
    db_session: AsyncSession, task_data: TaskCreate
) -> TaskResponse:
    return TaskResponse.model_validate(
        await create_task(db_session, task_data.model_dump())
    )


async def update_existing_task(
    db_session: AsyncSession, task_id: int, task_data: TaskUpdate
) -> TaskResponse:
    if not (task := await get_task_by_id(db_session, task_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if (task_data.status == StatusEnum.completed) and (
        task.status != StatusEnum.completed
    ):
        send_email_task.delay(
            subject=f"✅ Task completed: {task.title}",
            email_to=settings.ADMIN_EMAIL,
            body=f"<h1>Congratulations!</h1><p>The task <b>{task.title}</b> has been successfully marked as completed.</p>",
        )
    return TaskResponse.model_validate(
        await update_task(db_session, task, task_data.model_dump())
    )


async def delete_existing_task(db_session: AsyncSession, task_id: int) -> None:
    if task := await get_task_by_id(db_session, task_id):
        await delete_task(db_session, task)
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


async def get_task_history_service(
    db_session: AsyncSession, task_id: int
) -> list[TaskHistoryResponse]:
    if not await get_task_by_id(db_session, task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return [
        TaskHistoryResponse.model_validate(h)
        for h in await get_task_history(db_session, task_id)
    ]
