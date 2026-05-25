import uuid
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, sessionmaker, Session
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, func

from app.core.config import settings

engine = create_async_engine(url=settings.database_url, pool_size=10, max_overflow=20)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"
