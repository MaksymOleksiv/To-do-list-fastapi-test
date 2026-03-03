from typing import Sequence
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.models.task_history import TaskHistory
from app.core.config import StatusEnum


async def get_all_tasks(
    db: AsyncSession,
    status: StatusEnum | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Task]:
    query = select(Task)

    if status:
        query = query.where(Task.status == status)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def create_task(db: AsyncSession, task: dict) -> Task:
    task = Task(**task)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(db: AsyncSession, task: Task, task_data: dict) -> Task | None:
    for key, value in task_data.items():
        setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task: Task) -> Task | None:
    await db.delete(task)
    await db.commit()
    return task


async def delete_expired_tasks(db: AsyncSession) -> Sequence[Task]:
    stmt = (
        delete(Task)
        .where(Task.due_date < func.now(), Task.status != StatusEnum.completed)
        .returning(Task)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().all()


async def get_task_history(db: AsyncSession, task_id: int) -> Sequence[TaskHistory]:
    result = await db.execute(
        select(TaskHistory)
        .where(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.changed_at.desc())
    )
    return result.scalars().all()
