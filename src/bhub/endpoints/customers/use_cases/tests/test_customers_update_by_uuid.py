import pytest

from bhub.endpoints.customers.use_cases.customers_update_by_uuid import CustomersUpdateByUuidUseCase
from bhub.endpoints.exceptions import CustomerNotFoundException
from tests.factories import CustomersFactory


@pytest.mark.asyncio
async def test_successfully_run(customers_update_by_uuid_use_case: CustomersUpdateByUuidUseCase,
                                customer_payload: dict):

    customer_mock = CustomersFactory(company_name='Razao Social', billing=10000.5, phone_number='11 97967-0475',
                                     address='Rua lalalend, 123')

    customers_update_by_uuid_use_case._customers_service.get_by_params.return_value = CustomersFactory(
        uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')
    customers_update_by_uuid_use_case._customers_service.update_by_params.return_value = customer_mock

    await customers_update_by_uuid_use_case.run(tracking_id='tracking_id', schema=customer_payload['object'],
                                                customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    customers_update_by_uuid_use_case._customers_service.get_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=dict(uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823'))
    customers_update_by_uuid_use_case._customers_service.update_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=customer_payload['object'].dict(),
        uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')


@pytest.mark.asyncio
async def test_failed_run_customer_not_found(customers_update_by_uuid_use_case: CustomersUpdateByUuidUseCase,
                                             customer_payload: dict):

    customers_update_by_uuid_use_case._customers_service.get_by_params.return_value = None

    with pytest.raises(CustomerNotFoundException) as e:
        await customers_update_by_uuid_use_case.run(tracking_id='tracking_id', schema=customer_payload['object'],
                                                    customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert e.value.args[0] == {'title': 'Customer not found',
                               'detail': 'Customer ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823 does not exists'}
    customers_update_by_uuid_use_case._customers_service.get_by_params.assert_called_once()
    customers_update_by_uuid_use_case._customers_service.update_by_params.assert_not_called()
