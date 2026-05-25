from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SMeasurementAdd(BaseModel):
    x: float = Field(description='X axis value')
    y: float = Field(description='Y axis value')
    z: float = Field(description='Z axis value')


class SMeasurementAddDB(SMeasurementAdd):
    device_id: UUID


class SFieldStats(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float


class SStatsResponse(BaseModel):
    x: SFieldStats
    y: SFieldStats
    z: SFieldStats


class SDeviceStatsResponse(BaseModel):
    device_id: UUID
    device_name: str
    stats: SStatsResponse
    model_config = ConfigDict(from_attributes=True)

