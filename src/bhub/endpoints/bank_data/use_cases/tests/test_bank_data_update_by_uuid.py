import pytest

from bhub.endpoints.bank_data.use_cases.bank_data_update_by_uuid import BankDataUpdateByUuidUseCase
from bhub.endpoints.exceptions import BankDataNotFoundException
from tests.factories import BankDataFactory


@pytest.mark.asyncio
async def test_successfully_run(bank_data_update_by_uuid_use_case: BankDataUpdateByUuidUseCase,
                                bank_data_payload: dict):
    bank_data_mock = BankDataFactory(agency='0001', account='000000001', bank='nome do banco')

    bank_data_update_by_uuid_use_case._bank_data_service.get_by_uuid.return_value = BankDataFactory(
        uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')
    bank_data_update_by_uuid_use_case._bank_data_service.update_by_params.return_value = bank_data_mock

    await bank_data_update_by_uuid_use_case.run(tracking_id='tracking_id', schema=bank_data_payload['object'],
                                                bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')

    bank_data_update_by_uuid_use_case._bank_data_service.get_by_uuid.assert_called_once_with(
        tracking_id='tracking_id', uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')
    bank_data_update_by_uuid_use_case._bank_data_service.update_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=bank_data_payload['object'].dict(),
        uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.asyncio
async def test_failed_run_bank_data_not_found(bank_data_update_by_uuid_use_case: BankDataUpdateByUuidUseCase,
                                              bank_data_payload: dict):
    bank_data_update_by_uuid_use_case._bank_data_service.get_by_uuid.return_value = None

    with pytest.raises(BankDataNotFoundException) as e:
        await bank_data_update_by_uuid_use_case.run(tracking_id='tracking_id', schema=bank_data_payload['object'],
                                                    bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert e.value.args[0] == {'title': 'Bank data not found',
                               'detail': 'Bank data bb0e1a57-6f16-410c-89c4-6b18888810d3 does not exists'}
    bank_data_update_by_uuid_use_case._bank_data_service.get_by_uuid.assert_called_once()
    bank_data_update_by_uuid_use_case._bank_data_service.update_by_params.assert_not_called()
