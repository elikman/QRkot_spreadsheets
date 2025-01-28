from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


class CRUDBase:
    """Базовый класс для базовых операций с базой данных."""

    def __init__(self, model):
        self.model = model

    async def get(self, object_id: int, session: AsyncSession):
        db_object = await session.execute(
            select(self.model).where(object_id == self.model.id)
        )
        return db_object.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
        self,
        object_in: BaseModel,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_objects = self.model(**object_in_data)
        session.add(db_objects)
        await session.commit()
        await session.refresh(db_objects)
        return db_objects

    async def update(
        self,
        db_object: Base,
        object_in: BaseModel,
        session: AsyncSession
    ):
        # Representing the object from the database in a dictionary
        db_data = jsonable_encoder(db_object)
        # Converting an object with query data to a dictionary
        # And exclude the fields not set by the user
        new_data = object_in.dict(exclude_unset=True)
        for field in db_data:
            if field in new_data:
                setattr(db_object, field, new_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(self, db_object: Base, session: AsyncSession):
        await session.delete(db_object)
        await session.commit()
        return db_object
