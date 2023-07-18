import pytest

from datetime import datetime

from bhub.endpoints.customers.schemas import CustomerResponse


@pytest.fixture
def customer_response():
    dict_response = {'uuid': 'ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823', 'address': 'Rua lalalend, 123',
                     'created_at': datetime.strptime('2023-01-01T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ'),
                     'company_name': 'Razao Social', 'billing': 10000.50, 'phone_number': '1197967-0475'}
    return {'dict': dict_response, 'object': CustomerResponse(**dict_response)}
