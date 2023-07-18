import pytest
from starlette import status

from bhub.endpoints.exceptions import BankDataAlreadyExistsException, BankDataNotFoundException


@pytest.mark.asyncio
async def test_bank_data_create_successfully(mocker, client, bank_data_create_payload: dict, bank_data_response: dict):
    bank_data_create_use_case_mock = mocker.patch(
        'bhub.endpoints.bank_data.use_cases.bank_data_create.BankDataCreateUseCase.run',
        return_value=bank_data_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.post('/v1/bank-data', headers=headers, json=bank_data_create_payload['dict'])

    assert response.json() == bank_data_response['object'].dict()
    assert response.status_code == status.HTTP_201_CREATED
    bank_data_create_use_case_mock.assert_called_once_with(tracking_id='tracking_id',
                                                           schema=bank_data_create_payload['object'])


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [BankDataAlreadyExistsException, status.HTTP_409_CONFLICT,
     {'title': 'error title', 'detail': 'error_detail'}],
    [BankDataNotFoundException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while create bank data'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while create bank data'}]
])
@pytest.mark.asyncio
async def test_bank_data_create_exceptions(exception, expected_status_code, expected_response_json, mocker, client,
                                           bank_data_create_payload):
    mocker.patch('bhub.endpoints.bank_data.use_cases.bank_data_create.BankDataCreateUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.post('/v1/bank-data', json=bank_data_create_payload['dict'])

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


@pytest.mark.asyncio
async def test_bank_data_get_by_uuid_successfully(mocker, client, bank_data_response: dict):
    bank_data_get_by_uuid_use_case_mock = mocker.patch(
        'bhub.endpoints.bank_data.use_cases.bank_data_get_by_uuid.BankDataGetByUuidUseCase.run',
        return_value=bank_data_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.get('/v1/bank-data/bb0e1a57-6f16-410c-89c4-6b18888810d3', headers=headers)

    assert response.json() == bank_data_response['object'].dict()
    assert response.status_code == status.HTTP_200_OK
    bank_data_get_by_uuid_use_case_mock.assert_called_once_with(tracking_id='tracking_id',
                                                                bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [BankDataNotFoundException, status.HTTP_404_NOT_FOUND,
     {'title': 'error title', 'detail': 'error_detail'}],
    [BankDataAlreadyExistsException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while get bank data'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while get bank data'}]
])
@pytest.mark.asyncio
async def test_bank_data_get_by_uuid_exceptions(exception, expected_status_code, expected_response_json, mocker,
                                                client):
    mocker.patch('bhub.endpoints.bank_data.use_cases.bank_data_get_by_uuid.BankDataGetByUuidUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.get('/v1/bank-data/bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


@pytest.mark.asyncio
async def test_bank_data_update_by_uuid_successfully(mocker, client, bank_data_payload: dict, bank_data_response: dict):
    bank_data_update_by_uuid_use_case_mock = mocker.patch(
        'bhub.endpoints.bank_data.use_cases.bank_data_update_by_uuid.BankDataUpdateByUuidUseCase.run',
        return_value=bank_data_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.patch('/v1/bank-data/bb0e1a57-6f16-410c-89c4-6b18888810d3', headers=headers,
                                  json=bank_data_payload['dict'])

    assert response.json() == {'message': 'Bank data successfully updated'}
    assert response.status_code == status.HTTP_200_OK
    bank_data_update_by_uuid_use_case_mock.assert_called_once_with(
        tracking_id='tracking_id', schema=bank_data_payload['object'],
        bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [BankDataNotFoundException, status.HTTP_404_NOT_FOUND,
     {'title': 'error title', 'detail': 'error_detail'}],
    [BankDataAlreadyExistsException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while update bank data'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while update bank data'}]
])
@pytest.mark.asyncio
async def test_bank_data_update_by_uuid_exceptions(exception, expected_status_code, expected_response_json, mocker,
                                                   client, bank_data_payload):
    mocker.patch('bhub.endpoints.bank_data.use_cases.bank_data_update_by_uuid.BankDataUpdateByUuidUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.patch('/v1/bank-data/bb0e1a57-6f16-410c-89c4-6b18888810d3', json=bank_data_payload['dict'])

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


@pytest.mark.asyncio
async def test_bank_data_delete_by_uuid_successfully(mocker, client, bank_data_response: dict):
    bank_data_delete_by_uuid_use_case_mock = mocker.patch(
        'bhub.endpoints.bank_data.use_cases.bank_data_delete_by_uuid.BankDataDeleteByUuidUseCase.run',
        return_value=bank_data_response['dict'])

    headers = dict(requestId='tracking_id')

    response = await client.delete('/v1/bank-data/bb0e1a57-6f16-410c-89c4-6b18888810d3', headers=headers)

    assert response.json() == {'message': 'Bank data successfully deleted'}
    assert response.status_code == status.HTTP_200_OK
    bank_data_delete_by_uuid_use_case_mock.assert_called_once_with(
        tracking_id='tracking_id', bank_data_uuid='bb0e1a57-6f16-410c-89c4-6b18888810d3')


@pytest.mark.parametrize('exception, expected_status_code, expected_response_json', [
    [BankDataNotFoundException, status.HTTP_404_NOT_FOUND,
     {'title': 'error title', 'detail': 'error_detail'}],
    [BankDataAlreadyExistsException, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while delete bank data'}],
    [Exception, status.HTTP_500_INTERNAL_SERVER_ERROR,
     {'title': 'Internal error', 'detail': 'Error while delete bank data'}]
])
@pytest.mark.asyncio
async def test_bank_data_delete_by_uuid_exceptions(exception, expected_status_code, expected_response_json, mocker,
                                                   client):
    mocker.patch('bhub.endpoints.bank_data.use_cases.bank_data_delete_by_uuid.BankDataDeleteByUuidUseCase.run',
                 side_effect=exception({'title': 'error title', 'detail': 'error_detail'}))

    response = await client.delete('/v1/bank-data/bb0e1a57-6f16-410c-89c4-6b18888810d3')

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json
