from typing import AsyncGenerator
from sqlalchemy import NullPool, event
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Session
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, poolclass=NullPool)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        await session.commit()
        await session.close()


class Base(DeclarativeBase):
    pass


TRACKED_MODELS: set[str] = {"Task"}

IGNORED_FIELDS: set[str] = {"id", "created_at", "updated_at"}


@event.listens_for(Session, "before_flush")
def track_changes(session: Session, flush_context, instances) -> None:
    from app.models.task_history import TaskHistory

    for obj in session.dirty:
        if type(obj).__name__ not in TRACKED_MODELS:
            continue

        entries = []

        for column in obj.__table__.columns:
            field = column.key

            if field in IGNORED_FIELDS:
                continue

            hist = get_history(obj, field)

            if not hist.has_changes():
                continue

            old_value = hist.deleted[0] if hist.deleted else None
            new_value = hist.added[0] if hist.added else None

            if old_value == new_value:
                continue

            entries.append(
                TaskHistory(
                    task_id=obj.id,
                    field=field,
                    old_value=str(old_value) if old_value is not None else None,
                    new_value=str(new_value) if new_value is not None else None,
                )
            )

        session.add_all(entries)
