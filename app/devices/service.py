from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.devices.dao import DeviceDAO
from app.devices.schemas import SDeviceAdd, SDeviceAddDB, SDeviceUpdate, SDeviceInfo
from app.core.exceptions import DeviceNotFoundException


class DeviceService:
    def __init__(self, session: AsyncSession):
        self.device_dao = DeviceDAO(session)

    async def get_all_devices(self, user_id: UUID) -> list[SDeviceInfo]:
        devices = await self.device_dao.find_all_by_user(user_id)
        return [SDeviceInfo.model_validate(d) for d in devices]

    async def add_device(self, user_id: UUID, device_data: SDeviceAdd) -> SDeviceInfo:
        device = await self.device_dao.add(
            values=SDeviceAddDB(user_id=user_id, name=device_data.name)
        )
        return SDeviceInfo.model_validate(device)

    async def update_device(self, device_id: UUID, user_id: UUID, device_data: SDeviceUpdate) -> dict:
        device = await self.device_dao.update_device(
            device_id=device_id,
            user_id=user_id,
            name=device_data.name
        )
        if not device:
            raise DeviceNotFoundException
        return {'message': 'Device updated successfully'}

    async def delete_device(self, device_id: UUID, user_id: UUID) -> dict:
        deleted = await self.device_dao.delete_device(
            device_id=device_id,
            user_id=user_id
        )
        if not deleted:
            raise DeviceNotFoundException
        return {'message': 'Device deleted successfully'}
