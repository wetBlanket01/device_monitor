from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import MeasurementsNotFoundException
from app.tasks.stats import calculate_device_stats, calculate_stats_each_device
from app.devices.dao import DeviceDAO


class UserStatsService:
    def __init__(self, session: AsyncSession):
        self.device_dao = DeviceDAO(session)

    async def start_aggregated_stats(self, user_id: UUID) -> dict:
        devices = await self.device_dao.find_all_by_user(user_id)
        if not devices:
            raise MeasurementsNotFoundException

        task = calculate_device_stats.delay(
            device_ids=[str(d.id) for d in devices]
        )

        return {'task_id': task.id}

    async def start_stats_each_device(self, user_id: UUID) -> dict:
        devices = await self.device_dao.find_all_by_user(user_id)
        if not devices:
            raise MeasurementsNotFoundException

        task = calculate_stats_each_device.delay(
            device_ids=[str(d.id) for d in devices]
        )

        return {'task_id': task.id}
