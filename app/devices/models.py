from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Device(Base):
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
