from bhub.endpoints.base_use_case import BaseUseCase
from bhub.endpoints.customers.schemas import CustomersUpdatePayload
from bhub.endpoints.exceptions import CustomerNotFoundException
from bhub.logger import Logger
from bhub.services.customers_service import CustomersService


class CustomersUpdateByUuidUseCase(BaseUseCase):
    def __init__(self, customers_service: CustomersService, logger: Logger) -> None:
        self._customers_service = customers_service
        self._logger = logger

    async def run(self, tracking_id: str, customer_uuid: str, schema: CustomersUpdatePayload):
        self._logger.info(f'[{tracking_id}] Running get customer by uuid use case')

        customer = await self._customers_service.get_by_params(tracking_id=tracking_id, params=dict(uuid=customer_uuid))

        if not customer:
            self._logger.error(f'[{tracking_id}] Customer not found for uuid: {customer_uuid}')
            raise CustomerNotFoundException({'title': 'Customer not found',
                                            'detail': f'Customer {customer_uuid} does not exists'})

        self._logger.info(f'[{tracking_id}] Customer successfully retrieved')

        values = schema.dict(exclude_none=True)
        self._logger.debug(f'[{tracking_id}] Update values: {values}')
        await self._customers_service.update_by_params(tracking_id=tracking_id, params=values, uuid=customer.uuid)
        self._logger.info(f'[{tracking_id}] Customer successfully updated')
