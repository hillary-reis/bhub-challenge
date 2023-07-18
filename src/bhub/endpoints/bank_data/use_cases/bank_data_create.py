from bhub.logger import Logger

from bhub.endpoints.base_use_case import BaseUseCase
from bhub.endpoints.bank_data.schemas import BankDataCreatePayload
from bhub.endpoints.exceptions import BankDataAlreadyExistsException, CustomerNotFoundException
from bhub.infrastructure.models.bank_data import BankData
from bhub.services.bank_data_service import BankDataService
from bhub.services.customers_service import CustomersService


class BankDataCreateUseCase(BaseUseCase):
    def __init__(self, bank_data_service: BankDataService, customers_service: CustomersService, logger: Logger) -> None:
        self._bank_data_service = bank_data_service
        self._customers_service = customers_service
        self._logger = logger

    async def run(self, schema: BankDataCreatePayload, tracking_id: str) -> BankData:
        self._logger.info(f'[{tracking_id}] Running create bank data use case')
        schema_dict = schema.dict()
        customer_uuid = schema_dict.pop('customer_uuid')

        customer = await self._customers_service.get_by_params(tracking_id=tracking_id, params=dict(uuid=customer_uuid))

        if not customer:
            self._logger.error(f'[{tracking_id}] Customer not found for uuid: {customer_uuid}')
            raise CustomerNotFoundException({'title': 'Customer not found',
                                            'detail': f'Customer {customer_uuid} does not exists'})

        bank_data = await self._bank_data_service.get_by_params(tracking_id=tracking_id,
                                                                params=dict(bank=schema_dict['bank']))

        if bank_data:
            self._logger.error(f'[{tracking_id}] Customer {customer_uuid} already has a bank data for bank '
                               f'{schema_dict["bank"]}')
            raise BankDataAlreadyExistsException({'title': 'Bank data already exists',
                                                  'detail': 'Bank data already exists with this bank'})

        schema_dict['customer_id'] = customer.id

        bank_data = await self._bank_data_service.create(tracking_id=tracking_id, bank_data=schema_dict)
        self._logger.info(f'[{tracking_id}] Bank data successfully created')
        bank_data.customer_uuid = customer_uuid
        return bank_data
