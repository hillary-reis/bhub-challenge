import pytest

from datetime import datetime

from bhub.endpoints.bank_data.schemas import BankDataCreatePayload, BankDataResponse


@pytest.fixture
def bank_data_response():
    dict_response = {'uuid': 'bb0e1a57-6f16-410c-89c4-6b18888810d3', 'agency': '0001', 'account': '000000001',
                     'created_at': datetime.strptime('2023-01-01T01:01:01.001Z', '%Y-%m-%dT%H:%M:%S.%fZ'),
                     'bank': 'nome do banco', 'customer_uuid': 'ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823'}
    return {'dict': dict_response, 'object': BankDataResponse(**dict_response)}
