from bhub.endpoints.base_use_case import BaseUseCase
from bhub.endpoints.exceptions import BankDataNotFoundException
from bhub.logger import Logger
from bhub.services.bank_data_service import BankDataService


class BankDataDeleteByUuidUseCase(BaseUseCase):
    def __init__(self, bank_data_service: BankDataService, logger: Logger) -> None:
        self._bank_data_service = bank_data_service
        self._logger = logger

    async def run(self, tracking_id: str, bank_data_uuid: str):
        self._logger.info(f'[{tracking_id}] Running get bank_data by uuid use case')

        bank_data = await self._bank_data_service.get_by_uuid(tracking_id=tracking_id, uuid=bank_data_uuid)

        if not bank_data:
            self._logger.error(f'[{tracking_id}] Bank data not found for uuid: {bank_data_uuid}')
            raise BankDataNotFoundException({'title': 'Bank data not found',
                                            'detail': f'Bank data {bank_data_uuid} does not exists'})

        self._logger.info(f'[{tracking_id}] Bank data successfully retrieved')

        self._logger.debug(f'[{tracking_id}] Delete bank data')
        await self._bank_data_service.delete(tracking_id=tracking_id, bank_data=bank_data)
        self._logger.info(f'[{tracking_id}] Bank data successfully deleted')
