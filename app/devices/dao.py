from uuid import UUID
from sqlalchemy import select, delete

from app.dao.base import BaseDAO
from app.devices.models import Device


class DeviceDAO(BaseDAO):
    model = Device

    async def find_all_by_user(self, user_id: UUID) -> list[Device]:
        query = select(self.model).where(Device.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_by_id_and_user(self, device_id: UUID, user_id: UUID) -> Device | None:
        query = select(Device).where(
            Device.id == device_id,
            Device.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_device(self, device_id: UUID, user_id: UUID, name: str) -> Device | None:
        device = await self.find_by_id_and_user(device_id, user_id)
        if not device:
            return None
        device.name = name
        return device

    async def delete_device(self, device_id: UUID, user_id: UUID) -> bool:
        device = await self.find_by_id_and_user(device_id, user_id)
        if not device:
            return False
        await self.session.delete(device)
        return True
