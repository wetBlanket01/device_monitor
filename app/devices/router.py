from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.auth.dependencies import get_current_user
from app.devices.schemas import SDeviceAdd, SDeviceUpdate, SDeviceInfo
from app.devices.service import DeviceService
from app.users.models import User

router = APIRouter()


@router.get(path='/', response_model=list[SDeviceInfo])
async def get_devices(
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_without_commit)]
):
    return await DeviceService(session).get_all_devices(user.id)


@router.post(path='/')
async def add_device(
        device_data: SDeviceAdd,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_with_commit)]
):
    return await DeviceService(session).add_device(user.id, device_data)


@router.put(path='/{device_id}/')
async def update_device(
        device_id: UUID,
        device_data: SDeviceUpdate,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_with_commit)]
):
    return await DeviceService(session).update_device(device_id, user.id, device_data)


@router.delete(path='/{device_id}/')
async def delete_device(
        device_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_with_commit)]
):
    return await DeviceService(session).delete_device(device_id, user.id)
