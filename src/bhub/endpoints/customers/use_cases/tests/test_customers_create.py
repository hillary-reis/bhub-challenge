import pytest

from bhub.endpoints.customers.use_cases.customers_create import CustomersCreateUseCase
from bhub.endpoints.exceptions import CustomerAlreadyExistsException
from tests.factories import CustomersFactory


@pytest.mark.asyncio
async def test_successfully_run_create_customer(customers_create_use_case: CustomersCreateUseCase,
                                                customer_payload: dict):

    customer_mock = CustomersFactory()
    customers_create_use_case._customers_service.get_by_params.return_value = None
    customers_create_use_case._customers_service.create.return_value = customer_mock

    response = await customers_create_use_case.run(schema=customer_payload['object'], tracking_id='tracking_id')

    assert response == customer_mock

    customers_create_use_case._customers_service.get_by_params.assert_called_once_with(
        tracking_id='tracking_id', params=dict(company_name='Razao Social'))
    customers_create_use_case._customers_service.create.assert_called_once_with(
        tracking_id='tracking_id', customer=customer_payload['object'])


@pytest.mark.asyncio
async def test_failed_run_customer_already_exists(customers_create_use_case: CustomersCreateUseCase,
                                                  customer_payload: dict):

    customers_create_use_case._customers_service.get_by_params.return_value = CustomersFactory()

    with pytest.raises(CustomerAlreadyExistsException) as e:
        await customers_create_use_case.run(schema=customer_payload['object'], tracking_id='tracking_id')

    assert e.value.args[0] == {'title': 'Customer already exists',
                               'detail': 'Customer already exists with this company name'}
    customers_create_use_case._customers_service.get_by_params.assert_called_once()
    customers_create_use_case._customers_service.update_by_params.assert_not_called()
    customers_create_use_case._customers_service.create.assert_not_called()
