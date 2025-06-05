"""
Database configuration and session management only.
Single Responsibility: Database connection management.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .settings import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session factory
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    Single Responsibility: Provide database session.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_and_tables():
    """
    Create database tables.
    Single Responsibility: Database schema creation.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """
    Close database connections.
    Single Responsibility: Database cleanup.
    """
    await engine.dispose()