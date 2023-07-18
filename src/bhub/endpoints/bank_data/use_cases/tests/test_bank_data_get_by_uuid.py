import pytest

from bhub.endpoints.bank_data.use_cases.bank_data_get_by_uuid import BankDataGetByUuidUseCase
from bhub.endpoints.exceptions import BankDataNotFoundException
from tests.factories import BankDataFactory


@pytest.mark.asyncio
async def test_successfully_run(bank_data_get_by_uuid_use_case: BankDataGetByUuidUseCase):
    bank_data_mock = BankDataFactory()
    bank_data_get_by_uuid_use_case._bank_data_service.get_by_uuid.return_value = bank_data_mock

    response = await bank_data_get_by_uuid_use_case.run(tracking_id='tracking_id',
                                                        bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert response == bank_data_mock

    bank_data_get_by_uuid_use_case._bank_data_service.get_by_uuid.assert_called_once_with(
        tracking_id='tracking_id', uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.asyncio
async def test_failed_run_bank_data_not_found(bank_data_get_by_uuid_use_case: BankDataGetByUuidUseCase):
    bank_data_get_by_uuid_use_case._bank_data_service.get_by_uuid.return_value = None

    with pytest.raises(BankDataNotFoundException) as e:
        await bank_data_get_by_uuid_use_case.run(tracking_id='tracking_id',
                                                 bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert e.value.args[0] == {'title': 'Bank data not found',
                               'detail': 'Bank data bb0e1a57-6f16-410c-89c4-6b18888810d3 does not exists'}
    bank_data_get_by_uuid_use_case._bank_data_service.get_by_uuid.assert_called_once()
