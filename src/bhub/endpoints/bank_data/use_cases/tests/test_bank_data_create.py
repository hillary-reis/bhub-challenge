import pytest

from bhub.endpoints.bank_data.use_cases.bank_data_create import BankDataCreateUseCase
from bhub.endpoints.exceptions import BankDataAlreadyExistsException, CustomerNotFoundException
from tests.factories import BankDataFactory, CustomersFactory


@pytest.mark.asyncio
async def test_successfully_run(bank_data_create_use_case: BankDataCreateUseCase, bank_data_create_payload: dict):
    bank_data_mock = BankDataFactory()
    customer_mock = CustomersFactory()
    bank_data_create_use_case._customers_service.get_by_params.return_value = customer_mock
    bank_data_create_use_case._bank_data_service.get_by_params.return_value = None
    bank_data_create_use_case._bank_data_service.create.return_value = bank_data_mock

    response = await bank_data_create_use_case.run(schema=bank_data_create_payload['object'], tracking_id='tracking_id')

    assert response == bank_data_mock

    bank_data_create_use_case._customers_service.get_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=dict(uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823'))
    bank_data_create_use_case._bank_data_service.get_by_params.assert_called_once_with(
        tracking_id='tracking_id', params={'bank': 'nome do banco'})
    payload = bank_data_create_payload['object'].dict()
    payload['customer_id'] = customer_mock.id
    payload.pop('customer_uuid')
    bank_data_create_use_case._bank_data_service.create.assert_called_once_with(
        tracking_id='tracking_id', bank_data=payload)


@pytest.mark.asyncio
async def test_failed_run_customer_not_found(bank_data_create_use_case: BankDataCreateUseCase,
                                                   bank_data_create_payload: dict):

    bank_data_create_use_case._customers_service.get_by_params.return_value = None

    with pytest.raises(CustomerNotFoundException) as e:
        await bank_data_create_use_case.run(schema=bank_data_create_payload['object'], tracking_id='tracking_id')

    assert e.value.args[0] == {'title': 'Customer not found',
                               'detail': 'Customer ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823 does not exists'}
    bank_data_create_use_case._customers_service.get_by_params.assert_called_once()
    bank_data_create_use_case._bank_data_service.get_by_params.assert_not_called()
    bank_data_create_use_case._bank_data_service.create.assert_not_called()


@pytest.mark.asyncio
async def test_failed_run_bank_data_already_exists(bank_data_create_use_case: BankDataCreateUseCase,
                                                   bank_data_create_payload: dict):

    bank_data_create_use_case._customers_service.get_by_params.return_value = CustomersFactory()
    bank_data_create_use_case._bank_data_service.get_by_params.return_value = BankDataFactory()

    with pytest.raises(BankDataAlreadyExistsException) as e:
        await bank_data_create_use_case.run(schema=bank_data_create_payload['object'], tracking_id='tracking_id')

    assert e.value.args[0] == {'title': 'Bank data already exists',
                               'detail': 'Bank data already exists with this bank'}
    bank_data_create_use_case._customers_service.get_by_params.assert_called_once()
    bank_data_create_use_case._bank_data_service.get_by_params.assert_called_once()
    bank_data_create_use_case._bank_data_service.create.assert_not_called()
