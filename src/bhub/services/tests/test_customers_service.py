import pytest

from bhub.services.customers_service import CustomersService

from tests.factories import CustomersFactory


@pytest.mark.asyncio
async def test_create_successfully(customers_service: CustomersService, customer_payload: dict):
    customer_mock = CustomersFactory()
    customers_service._customers_sql_repository.create.return_value = customer_mock
    customer = await customers_service.create(tracking_id='tracking_id', customer=customer_payload['object'])

    assert customer == customer_mock
    customers_service._customers_sql_repository.create.assert_called_once_with(values=customer_payload['object'].dict())


@pytest.mark.asyncio
async def test_get_by_params_successfully(customers_service: CustomersService, customer_payload: dict):
    customer_mock = CustomersFactory()
    customers_service._customers_sql_repository.filter_by.return_value = customer_mock
    customer = await customers_service.get_by_params(tracking_id='tracking_id', params=customer_payload['dict'])

    assert customer == customer_mock
    customers_service._customers_sql_repository.filter_by.assert_called_once_with(params=customer_payload['dict'])


@pytest.mark.asyncio
async def test_update_by_params_successfully(customers_service: CustomersService, customer_payload: dict):
    customer_mock = CustomersFactory()
    customers_service._customers_sql_repository.update.return_value = customer_mock
    customer = await customers_service.update_by_params(tracking_id='tracking_id', params=customer_payload['dict'],
                                                        uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert customer == customer_mock
    customers_service._customers_sql_repository.update.assert_called_once_with(
        values=customer_payload['dict'], pk='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')
