from bhub.infrastructure.models.customers import Customers

from bhub.infrastructure.repositories.sql_repository import SqlRepository


class CustomersSqlRepository(SqlRepository):
    model = Customers
