from bhub.infrastructure.models.bank_data import BankData
from bhub.logger import Logger
from bhub.repositories.bank_data_repository import BankDataSqlRepository


class BankDataService:
    def __init__(self, bank_data_sql_repository: BankDataSqlRepository, logger: Logger) -> None:
        self._bank_data_sql_repository = bank_data_sql_repository
        self.logger = logger

    async def create(self, tracking_id: str, bank_data: dict) -> BankData:
        self.logger.info(f'[{tracking_id}] Creating bank data')
        self.logger.debug(f'[{tracking_id}] bank infos: {bank_data}')
        return await self._bank_data_sql_repository.create(values=bank_data)

    async def get_by_bank_and_customer_uuid(self, tracking_id: str, bank: str, customer_uuid: str) -> BankData | None:
        self.logger.info(f'[{tracking_id}] Getting bank data by params')
        self.logger.debug(f'[{tracking_id}] Bank: {bank} | customer: {customer_uuid}')
        return await self._bank_data_sql_repository.find_by_bank_and_customer_uuid(customer_uuid=customer_uuid,
                                                                                   bank=bank)

    async def get_by_uuid(self, tracking_id: str, uuid: str) -> BankData | None:
        self.logger.info(f'[{tracking_id}] Getting bank data by uuid: {uuid}')
        return await self._bank_data_sql_repository.find_by_uuid(uuid=uuid)

    async def get_by_params(self, tracking_id: str, params: dict) -> BankData | None:
        self.logger.info(f'[{tracking_id}] Getting bank data by params')
        self.logger.debug(f'[{tracking_id}] Params: {params}')
        return await self._bank_data_sql_repository.filter_by(params=params)

    async def update_by_params(self, tracking_id: str, uuid: str, params: dict):
        self.logger.info(f'[{tracking_id}] Updating bank data: {uuid}')
        self.logger.debug(f'[{tracking_id}] Params: {params}')
        return await self._bank_data_sql_repository.update(pk=uuid, values=params)

    async def delete(self, tracking_id: str, bank_data: BankData):
        self.logger.info(f'[{tracking_id}] Delete bank data')
        return await self._bank_data_sql_repository.delete(bank_data)
