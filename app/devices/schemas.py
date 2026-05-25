from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class DeviceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255, description='Device name')
    model_config = ConfigDict(from_attributes=True)


class SDeviceAdd(DeviceBase):
    pass


class SDeviceUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255, description='Device name')


class SDeviceAddDB(DeviceBase):
    user_id: UUID


class SDeviceInfo(DeviceBase):
    id: UUID
    user_id: UUID
