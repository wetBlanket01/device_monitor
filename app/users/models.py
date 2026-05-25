from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.dao.database import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
