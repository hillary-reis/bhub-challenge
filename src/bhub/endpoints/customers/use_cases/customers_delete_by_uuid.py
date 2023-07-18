from bhub.endpoints.base_use_case import BaseUseCase
from bhub.endpoints.exceptions import CustomerNotFoundException
from bhub.logger import Logger
from bhub.services.customers_service import CustomersService


class CustomersDeleteByUuidUseCase(BaseUseCase):
    def __init__(self, customers_service: CustomersService, logger: Logger) -> None:
        self._customers_service = customers_service
        self._logger = logger

    async def run(self, tracking_id: str, customer_uuid: str):
        self._logger.info(f'[{tracking_id}] Running get customer by uuid use case')

        customer = await self._customers_service.get_by_params(tracking_id=tracking_id, params=dict(uuid=customer_uuid))

        if not customer:
            self._logger.error(f'[{tracking_id}] Customer not found for uuid: {customer_uuid}')
            raise CustomerNotFoundException({'title': 'Customer not found',
                                            'detail': f'Customer {customer_uuid} does not exists'})

        self._logger.info(f'[{tracking_id}] Customer successfully retrieved')

        self._logger.debug(f'[{tracking_id}] Delete customer')
        await self._customers_service.delete(tracking_id=tracking_id, customer=customer)
        self._logger.info(f'[{tracking_id}] Customer successfully deleted')
