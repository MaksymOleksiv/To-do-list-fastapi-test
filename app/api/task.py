from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import StatusEnum
from app.services.task import (
    get_tasks,
    get_task,
    create_new_task,
    update_existing_task,
    delete_existing_task,
)
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from app.core.db import get_db
from app.core.limiter import limiter

router = APIRouter()

db_session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/tasks", response_model=list[TaskResponse])
@limiter.limit("5/minute")
async def read_tasks(
    request: Request,
    db: db_session,
    status: StatusEnum | None = Query(
        None, description="Filter tasks by status (pending or completed)"
    ),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of items to return"),
) -> list[TaskResponse]:
    return await get_tasks(db, status=status, skip=skip, limit=limit)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit("5/minute")
async def read_task(request: Request, task_id: int, db: db_session) -> TaskResponse:
    return await get_task(db, task_id)


@router.post("/tasks", response_model=TaskResponse)
@limiter.limit("5/minute")
async def create_task(
    request: Request, task: TaskCreate, db: db_session
) -> TaskResponse:
    return await create_new_task(db, task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit("5/minute")
async def update_task(request: Request, task_id: int, task: TaskUpdate, db: db_session) -> TaskResponse:
    return await update_existing_task(db, task_id, task)


@router.delete("/tasks/{task_id}", status_code=204)
@limiter.limit("5/minute")
async def delete_task(request: Request, task_id: int, db: db_session) -> None:
    await delete_existing_task(db, task_id)
    return None
