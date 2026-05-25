from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.devices.dao import DeviceDAO
from app.measurements.dao import MeasurementDAO
from app.measurements.schemas import SMeasurementAdd, SMeasurementAddDB
from app.core.exceptions import DeviceNotFoundException

from app.tasks.stats import calculate_device_stats


class MeasurementService:
    def __init__(self, session: AsyncSession):
        self.device_dao = DeviceDAO(session)
        self.measurement_dao = MeasurementDAO(session)

    async def add_measurement(self, device_id: UUID, user_id: UUID, data: SMeasurementAdd) -> dict:
        device = await self.device_dao.find_by_id_and_user(device_id, user_id)
        if not device:
            raise DeviceNotFoundException

        await self.measurement_dao.add(
            values=SMeasurementAddDB(device_id=device_id, **data.model_dump())
        )
        return {'message': 'Measurement added successfully'}

    async def start_device_stats(
            self,
            device_id: UUID,
            user_id: UUID,
            from_dt: datetime | None = None,
            to_dt: datetime | None = None
    ) -> dict:
        device = await self.device_dao.find_by_id_and_user(device_id, user_id)
        if not device:
            raise DeviceNotFoundException

        task = calculate_device_stats.delay(
            device_ids=[str(device_id)],
            from_dt=from_dt,
            to_dt=to_dt
        )

        return {'task_id': task.id}
