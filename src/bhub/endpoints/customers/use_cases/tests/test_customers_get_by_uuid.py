import pytest

from bhub.endpoints.customers.use_cases.customers_get_by_uuid import CustomersGetByUuidUseCase
from bhub.endpoints.exceptions import CustomerNotFoundException
from tests.factories import CustomersFactory


@pytest.mark.asyncio
async def test_successfully_run(customers_get_by_uuid_use_case: CustomersGetByUuidUseCase):
    customer_mock = CustomersFactory()
    customers_get_by_uuid_use_case._customers_service.get_by_params.return_value = customer_mock

    response = await customers_get_by_uuid_use_case.run(tracking_id='tracking_id',
                                                        customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert response == customer_mock

    customers_get_by_uuid_use_case._customers_service.get_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=dict(uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823'))


@pytest.mark.asyncio
async def test_failed_run_customer_not_found(customers_get_by_uuid_use_case: CustomersGetByUuidUseCase):
    customers_get_by_uuid_use_case._customers_service.get_by_params.return_value = None

    with pytest.raises(CustomerNotFoundException) as e:
        await customers_get_by_uuid_use_case.run(tracking_id='tracking_id',
                                                 customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert e.value.args[0] == {'title': 'Customer not found',
                               'detail': 'Customer ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823 does not exists'}
    customers_get_by_uuid_use_case._customers_service.get_by_params.assert_called_once()
