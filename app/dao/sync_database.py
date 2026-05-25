from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

sync_engine = create_engine(url=settings.sync_database_url, pool_size=5, max_overflow=10, pool_pre_ping=True)
sync_session_maker = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)
