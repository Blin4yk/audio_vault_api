from fastapi import HTTPException
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import NoResultFound

from backend.config import async_session_maker


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)  # запрос в бд
            await session.commit()  # фиксирование

    @classmethod
    async def delete(cls, model_id):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    @classmethod
    async def update(cls, model_id, update_data: dict):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == model_id)
                .values(**update_data)
            )
            result = await session.execute(query)
            update_model = await result.scalar_one_or_none()
            await session.commit()
            return update_model