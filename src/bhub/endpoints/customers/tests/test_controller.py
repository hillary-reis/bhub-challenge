import pytest
from starlette import status

from bhub.endpoints.exceptions import CustomerAlreadyExistsException, CustomerNotFoundException


@pytest.mark.asyncio
async def test_customers_create_successfully(mocker, client, customer_payload: dict, customer_response: dict):
    customers_create_use_case_mock = mocker.patch(
        'bhub.endpoints.customers.use_cases.customers_create.CustomersCreateUseCase.run',
        return_value=customer_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.post('/v1/customers', headers=headers, json=customer_payload['dict'])

    assert response.json() == customer_response['object'].dict()
    assert response.status_code == status.HTTP_201_CREATED
    customers_create_use_case_mock.assert_called_once_with(tracking_id='tracking_id', schema=customer_payload['object'])


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [CustomerAlreadyExistsException, status.HTTP_409_CONFLICT,
     {'title': 'error title', 'detail': 'error_detail'}],
    [CustomerNotFoundException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while create customer'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while create customer'}]
])
@pytest.mark.asyncio
async def test_customers_create_exceptions(exception, expected_status_code, expected_response_json, mocker, client,
                                           customer_payload):
    mocker.patch('bhub.endpoints.customers.use_cases.customers_create.CustomersCreateUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.post('/v1/customers', json=customer_payload['dict'])

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


@pytest.mark.asyncio
async def test_customers_get_by_uuid_successfully(mocker, client, customer_response: dict):
    customers_get_by_uuid_use_case_mock = mocker.patch(
        'bhub.endpoints.customers.use_cases.customers_get_by_uuid.CustomersGetByUuidUseCase.run',
        return_value=customer_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.get('/v1/customers/ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823', headers=headers)

    assert response.json() == customer_response['object'].dict()
    assert response.status_code == status.HTTP_200_OK
    customers_get_by_uuid_use_case_mock.assert_called_once_with(tracking_id='tracking_id',
                                                                customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [CustomerNotFoundException, status.HTTP_404_NOT_FOUND,
     {'title': 'error title', 'detail': 'error_detail'}],
    [CustomerAlreadyExistsException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while get customer'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while get customer'}]
])
@pytest.mark.asyncio
async def test_customers_get_by_uuid_exceptions(exception, expected_status_code, expected_response_json, mocker,
                                                client):
    mocker.patch('bhub.endpoints.customers.use_cases.customers_get_by_uuid.CustomersGetByUuidUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.get('/v1/customers/ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


@pytest.mark.asyncio
async def test_customers_update_by_uuid_successfully(mocker, client, customer_payload: dict, customer_response: dict):
    customers_update_by_uuid_use_case_mock = mocker.patch(
        'bhub.endpoints.customers.use_cases.customers_update_by_uuid.CustomersUpdateByUuidUseCase.run',
        return_value=customer_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.patch('/v1/customers/ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823', headers=headers,
                                  json=customer_payload['dict'])

    assert response.json() == {'message': 'Customer successfully updated'}
    assert response.status_code == status.HTTP_200_OK
    customers_update_by_uuid_use_case_mock.assert_called_once_with(tracking_id='tracking_id',
                                                                   schema=customer_payload['object'],
                                                                   customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [CustomerNotFoundException, status.HTTP_404_NOT_FOUND,
     {'title': 'error title', 'detail': 'error_detail'}],
    [CustomerAlreadyExistsException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while update customer'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while update customer'}]
])
@pytest.mark.asyncio
async def test_customers_update_by_uuid_exceptions(exception, expected_status_code, expected_response_json, mocker,
                                                   client, customer_payload):
    mocker.patch('bhub.endpoints.customers.use_cases.customers_update_by_uuid.CustomersUpdateByUuidUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.patch('/v1/customers/ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823', json=customer_payload['dict'])

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


@pytest.mark.asyncio
async def test_customers_delete_by_uuid_successfully(mocker, client, customer_response: dict):
    customers_delete_by_uuid_use_case_mock = mocker.patch(
        'bhub.endpoints.customers.use_cases.customers_delete_by_uuid.CustomersDeleteByUuidUseCase.run',
        return_value=customer_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.delete('/v1/customers/ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823', headers=headers)

    assert response.json() == {'message': 'Customer successfully deleted'}
    assert response.status_code == status.HTTP_200_OK
    customers_delete_by_uuid_use_case_mock.assert_called_once_with(tracking_id='tracking_id',
                                                                   customer_uuid='ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [CustomerNotFoundException, status.HTTP_404_NOT_FOUND,
     {'title': 'error title', 'detail': 'error_detail'}],
    [CustomerAlreadyExistsException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while delete customer'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while delete customer'}]
])
@pytest.mark.asyncio
async def test_customers_delete_by_uuid_exceptions(exception, expected_status_code, expected_response_json, mocker,
                                                   client):
    mocker.patch('bhub.endpoints.customers.use_cases.customers_delete_by_uuid.CustomersDeleteByUuidUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.delete('/v1/customers/ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823')

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json
