from sqlalchemy import select, update

from bhub.infrastructure.database.sql import Base
from bhub.infrastructure.repositories.irepository import IRepository


class SqlRepository(IRepository):
    model = Base

    async def filter_by(self, params: dict):
        async with self.session_factory() as session:
            result = await session.execute(select(self.model).filter_by(**params))
            return result.scalars().first()

    async def create(self, values: dict):
        async with self.session_factory() as session:
            _model = self.model(**values)
            session.add(_model)
            await session.commit()
            return _model

    async def update(self, pk: str, values: dict):
        async with self.session_factory() as session:
            await session.execute(update(self.model).where(self.model.uuid == pk).values(**values))
            await session.commit()

    async def delete(self, _model: Base):
        async with self.session_factory() as session:
            await session.delete(_model)
            await session.commit()
