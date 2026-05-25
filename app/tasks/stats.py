from uuid import UUID
from sqlalchemy import select, func

from app.celery_app import celery_app
from app.dao.sync_database import sync_session_maker
from app.measurements.models import Measurement
from app.devices.models import Device
from app.measurements.schemas import SFieldStats, SStatsResponse, SDeviceStatsResponse


def _calc_stats_query(session, device_ids, from_dt=None, to_dt=None):
    query = select(
        func.min(Measurement.x), func.max(Measurement.x),
        func.count(Measurement.x), func.sum(Measurement.x),
        func.percentile_cont(0.5).within_group(Measurement.x),

        func.min(Measurement.y), func.max(Measurement.y),
        func.count(Measurement.y), func.sum(Measurement.y),
        func.percentile_cont(0.5).within_group(Measurement.y),

        func.min(Measurement.z), func.max(Measurement.z),
        func.count(Measurement.z), func.sum(Measurement.z),
        func.percentile_cont(0.5).within_group(Measurement.z),
    ).where(Measurement.device_id.in_(device_ids))

    if from_dt:
        query = query.where(Measurement.created_at >= from_dt)
    if to_dt:
        query = query.where(Measurement.created_at <= to_dt)

    return session.execute(query).one_or_none()


@celery_app.task(name='calculate_device_stats')
def calculate_device_stats(device_ids, from_dt=None, to_dt=None):
    ids = [UUID(d) for d in device_ids]
    with sync_session_maker() as session:
        row = _calc_stats_query(session, ids, from_dt, to_dt)

        if not row or row[2] == 0:
            return None

        return SStatsResponse(
            x=SFieldStats(min=row[0], max=row[1], count=row[2], sum=row[3], median=row[4]),
            y=SFieldStats(min=row[5], max=row[6], count=row[7], sum=row[8], median=row[9]),
            z=SFieldStats(min=row[10], max=row[11], count=row[12], sum=row[13], median=row[14]),
        ).model_dump()


@celery_app.task(name='calculate_stats_each_device')
def calculate_stats_each_device(device_ids):
    ids = [UUID(d) for d in device_ids]
    with sync_session_maker() as session:
        query = select(
            Measurement.device_id,
            Device.name,

            func.min(Measurement.x), func.max(Measurement.x),
            func.count(Measurement.x), func.sum(Measurement.x),
            func.percentile_cont(0.5).within_group(Measurement.x),

            func.min(Measurement.y), func.max(Measurement.y),
            func.count(Measurement.y), func.sum(Measurement.y),
            func.percentile_cont(0.5).within_group(Measurement.y),

            func.min(Measurement.z), func.max(Measurement.z),
            func.count(Measurement.z), func.sum(Measurement.z),
            func.percentile_cont(0.5).within_group(Measurement.z),
        ).join(Device, Measurement.device_id == Device.id
               ).where(Measurement.device_id.in_(ids)
                       ).group_by(Measurement.device_id, Device.name)

        rows = session.execute(query).all()

        return [
            SDeviceStatsResponse(
                device_id=row[0],
                device_name=row[1],
                stats=SStatsResponse(
                    x=SFieldStats(min=row[2], max=row[3], count=row[4], sum=row[5], median=row[6]),
                    y=SFieldStats(min=row[7], max=row[8], count=row[9], sum=row[10], median=row[11]),
                    z=SFieldStats(min=row[12], max=row[13], count=row[14], sum=row[15], median=row[16]),
                )
            ).model_dump()
            for row in rows
        ]
