import pytest

from bhub.endpoints.customers.use_cases.customers_delete_by_uuid import CustomersDeleteByUuidUseCase
from bhub.endpoints.exceptions import CustomerNotFoundException
from tests.factories import CustomersFactory


@pytest.mark.asyncio
async def test_successfully_run(customers_delete_by_uuid_use_case: CustomersDeleteByUuidUseCase):
    customer_mock = CustomersFactory()
    customers_delete_by_uuid_use_case._customers_service.get_by_params.return_value = customer_mock
    customers_delete_by_uuid_use_case._customers_service.delete.return_value = True

    await customers_delete_by_uuid_use_case.run(tracking_id='tracking_id',
                                                customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    customers_delete_by_uuid_use_case._customers_service.get_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=dict(uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823'))
    customers_delete_by_uuid_use_case._customers_service.delete.assert_called_once_with(
        tracking_id='tracking_id', customer=customer_mock)


@pytest.mark.asyncio
async def test_failed_run_customer_already_exists(customers_delete_by_uuid_use_case: CustomersDeleteByUuidUseCase):
    customers_delete_by_uuid_use_case._customers_service.get_by_params.return_value = None

    with pytest.raises(CustomerNotFoundException) as e:
        await customers_delete_by_uuid_use_case.run(tracking_id='tracking_id',
                                                    customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert e.value.args[0] == {'title': 'Customer not found',
                               'detail': 'Customer ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823 does not exists'}
    customers_delete_by_uuid_use_case._customers_service.get_by_params.assert_called_once()
    customers_delete_by_uuid_use_case._customers_service.update_by_params.assert_not_called()
