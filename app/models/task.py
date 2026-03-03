import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from app.core.db import Base
from app.core.config import StatusEnum





class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[StatusEnum] = mapped_column(
        nullable=False, server_default=StatusEnum.pending.value
    )
    due_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
