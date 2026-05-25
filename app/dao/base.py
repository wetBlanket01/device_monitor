from typing import TypeVar, Generic, Type

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select, update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .database import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        if self.model is None:
            raise ValueError("The model must be specified in the child class")

    async def find_one_or_none_by_id(self, data_id):
        try:
            query = select(self.model).filter_by(id=data_id)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            logger.error(f"Error while searching for a record with ID {data_id}: {e}")
            raise

    async def find_one_or_none(self, filters_dict: dict):
        try:
            query = select(self.model).filter_by(**filters_dict)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            logger.error(
                f"Error while searching for a record by filters {filters_dict}: {e}"
            )
            raise

    async def add(self, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        try:
            new_instance = self.model(**values_dict)
            self.session.add(new_instance)
            await self.session.flush()
            return new_instance
        except SQLAlchemyError as e:
            logger.error(f"Error while adding {values_dict}: {e}")
            raise

    async def update(self, values: dict, filters: dict):
        try:
            query = sqlalchemy_update(self.model).filter_by(**filters).values(**values)
            result = await self.session.execute(query)
            await self.session.flush()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error while updating {filters}: {e}")
            raise
