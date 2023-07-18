import pytest

from bhub.services.bank_data_service import BankDataService

from tests.factories import BankDataFactory


@pytest.mark.asyncio
async def test_create_successfully(bank_data_service: BankDataService, bank_data_payload: dict):
    bank_data_mock = BankDataFactory()
    bank_data_service._bank_data_sql_repository.create.return_value = bank_data_mock
    bank_data = await bank_data_service.create(tracking_id='tracking_id', bank_data=bank_data_payload['object'])

    assert bank_data == bank_data_mock
    bank_data_service._bank_data_sql_repository.create.assert_called_once_with(
        values=bank_data_payload['object'].dict())


@pytest.mark.asyncio
async def test_get_by_bank_and_customer_uuid_successfully(bank_data_service: BankDataService):
    bank_data_mock = BankDataFactory()
    bank_data_service._bank_data_sql_repository.find_by_bank_and_customer_uuid.return_value = bank_data_mock
    bank_data = await bank_data_service.get_by_bank_and_customer_uuid(
        tracking_id='tracking_id', bank='nome do banco', customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert bank_data == bank_data_mock
    bank_data_service._bank_data_sql_repository.find_by_bank_and_customer_uuid.assert_called_once_with(
        bank='nome do banco', customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')


@pytest.mark.asyncio
async def test_get_by_uuid_successfully(bank_data_service: BankDataService):
    bank_data_mock = BankDataFactory()
    bank_data_service._bank_data_sql_repository.find_by_uuid.return_value = bank_data_mock
    bank_data = await bank_data_service.get_by_uuid(tracking_id='tracking_id',
                                                    uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert bank_data == bank_data_mock
    bank_data_service._bank_data_sql_repository.find_by_uuid.assert_called_once_with(
        uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.asyncio
async def test_update_by_params_successfully(bank_data_service: BankDataService, bank_data_payload: dict):
    bank_data_mock = BankDataFactory()
    bank_data_service._bank_data_sql_repository.update.return_value = bank_data_mock
    bank_data = await bank_data_service.update_by_params(tracking_id='tracking_id', params=bank_data_payload['dict'],
                                                         uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert bank_data == bank_data_mock
    bank_data_service._bank_data_sql_repository.update.assert_called_once_with(
        values=bank_data_payload['dict'], pk='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.asyncio
async def test_delete_successfully(bank_data_service: BankDataService):
    bank_data_mock = BankDataFactory()
    bank_data_service._bank_data_sql_repository.delete.return_value = bank_data_mock
    bank_data = await bank_data_service.delete(tracking_id='tracking_id', bank_data=bank_data_mock)

    assert bank_data == bank_data_mock
    bank_data_service._bank_data_sql_repository.delete.assert_called_once_with(bank_data_mock)
