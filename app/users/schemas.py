from typing import Self
from uuid import UUID

from pydantic import BaseModel, model_validator, Field, ConfigDict

from app.auth.utils import get_password_hash


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50, description='Username, from 3 to 50 characters')

    model_config = ConfigDict(from_attributes=True)


class SUserRegister(UserBase):
    password: str = Field(min_length=5, max_length=50, description='Password, from 5 to 50 characters')
    confirm_password: str = Field(min_length=5, max_length=50, description='Confirm password')

    @model_validator(mode='after')
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        self.password = get_password_hash(self.password)
        return self


class SUserAddDB(UserBase):
    password_hash: str = Field(min_length=5, description='Password in format HASH-string')


class SUserAuth(UserBase):
    password: str = Field(min_length=5, max_length=50, description='Password, from 5 to 50 characters')


class SUserInfo(UserBase):
    id: UUID = Field(description='Id of the user')
