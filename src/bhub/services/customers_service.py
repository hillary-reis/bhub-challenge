from bhub.infrastructure.models.customers import Customers
from bhub.logger import Logger
from bhub.repositories.customers_repository import CustomersSqlRepository
from bhub.endpoints.customers.schemas import CustomersCreatePayload


class CustomersService:
    def __init__(self, customers_sql_repository: CustomersSqlRepository, logger: Logger) -> None:
        self._customers_sql_repository = customers_sql_repository
        self.logger = logger

    async def create(self, tracking_id: str, customer: CustomersCreatePayload) -> Customers:
        self.logger.info(f'[{tracking_id}] Creating customer')
        dict_customer = customer.dict()
        self.logger.debug(f'[{tracking_id}] customer infos: {dict_customer}')
        return await self._customers_sql_repository.create(values=dict_customer)

    async def get_by_params(self, tracking_id: str, params: dict) -> Customers | None:
        self.logger.info(f'[{tracking_id}] Getting customer by params')
        self.logger.debug(f'[{tracking_id}] Params: {params}')
        return await self._customers_sql_repository.filter_by(params=params)

    async def update_by_params(self, tracking_id: str, uuid: str, params: dict):
        self.logger.info(f'[{tracking_id}] Updating customer: {uuid}')
        self.logger.debug(f'[{tracking_id}] Params: {params}')
        return await self._customers_sql_repository.update(pk=uuid, values=params)

    async def delete(self, tracking_id: str, customer: Customers):
        self.logger.info(f'[{tracking_id}] Delete customer')
        return await self._customers_sql_repository.delete(customer)
