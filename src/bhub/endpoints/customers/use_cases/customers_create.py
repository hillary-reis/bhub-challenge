from bhub.logger import Logger

from bhub.endpoints.base_use_case import BaseUseCase
from bhub.endpoints.customers.schemas import CustomersCreatePayload
from bhub.endpoints.exceptions import CustomerAlreadyExistsException
from bhub.infrastructure.models.customers import Customers
from bhub.services.customers_service import CustomersService


class CustomersCreateUseCase(BaseUseCase):
    def __init__(self, customers_service: CustomersService, logger: Logger) -> None:
        self._customers_service = customers_service
        self._logger = logger

    async def run(self, schema: CustomersCreatePayload, tracking_id: str) -> Customers:
        self._logger.info(f'[{tracking_id}] Running create customer use case')

        customer = await self._customers_service.get_by_params(tracking_id=tracking_id,
                                                               params=dict(company_name=schema.company_name))

        if customer:
            self._logger.error(f'[{tracking_id}] Customer already exists with company name: {schema.company_name}')
            raise CustomerAlreadyExistsException({'title': 'Customer already exists',
                                                  'detail': 'Customer already exists with this company name'})

        customer = await self._customers_service.create(tracking_id=tracking_id, customer=schema)
        self._logger.info(f'[{tracking_id}] Customer successfully created')
        return customer
