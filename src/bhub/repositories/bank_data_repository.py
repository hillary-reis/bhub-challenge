from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bhub.infrastructure.models.bank_data import BankData
from bhub.infrastructure.models.customers import Customers
from bhub.infrastructure.repositories.sql_repository import SqlRepository


class BankDataSqlRepository(SqlRepository):
    model = BankData

    async def find_by_bank_and_customer_uuid(self, bank: str, customer_uuid: str) -> BankData | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model)
                .join(Customers, (Customers.id == self.model.customer_id))
                .filter(self.model.bank == bank, Customers.uuid == customer_uuid)
            )

            return result.scalars().first() or None

    async def find_by_uuid(self, uuid: str) -> BankData | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model)
                .filter(self.model.uuid == uuid)
                .options(joinedload(self.model.customer).load_only(Customers.uuid))
            )

            return result.scalars().first() or None
