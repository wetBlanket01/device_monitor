from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

from app.dao.database import Base


class Measurement(Base):
    device_id: Mapped[UUID] = mapped_column(ForeignKey('devices.id'), primary_key=True, index=True)
    x: Mapped[float] = mapped_column(nullable=False)
    y: Mapped[float] = mapped_column(nullable=False)
    z: Mapped[float] = mapped_column(nullable=False)
