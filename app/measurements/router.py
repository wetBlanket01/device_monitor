from uuid import UUID
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.auth.dependencies import get_current_user
from app.measurements.schemas import SMeasurementAdd
from app.measurements.service import MeasurementService
from app.users.models import User

router = APIRouter()


@router.post('/{device_id}/stats/')
async def add_measurement(
        device_id: UUID,
        data: SMeasurementAdd,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_with_commit)]
):
    return await MeasurementService(session).add_measurement(device_id, user.id, data)


@router.get('/{device_id}/stats/')
async def get_device_stats(
        device_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_without_commit)],
        from_dt: datetime | None = None,
        to_dt: datetime | None = None
):
    return await MeasurementService(session).start_device_stats(
        device_id, user.id, from_dt, to_dt
    )
