from typing import AsyncGenerator
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
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
