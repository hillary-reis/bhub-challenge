import pytest

from httpx import AsyncClient
from unittest.mock import MagicMock

from bhub.infrastructure.database.sql import PostgresDatabase
from bhub.endpoints.bank_data.schemas import BankDataCreatePayload, BankDataPayload
from bhub.endpoints.customers.schemas import CustomersPayload


@pytest.fixture
def db():
    PostgresDatabase.create_database = MagicMock()


@pytest.fixture
def app(db):
    from app import create_app
    app = create_app()
    yield app


@pytest.fixture
def client(event_loop, app):
    client = AsyncClient(app=app, base_url='http://test')
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.fixture
def bank_data_payload():
    dict_response = {'agency': '0001', 'account': '000000001', 'bank': 'nome do banco'}
    return {'dict': dict_response, 'object': BankDataPayload(**dict_response)}


@pytest.fixture
def bank_data_create_payload():
    dict_response = {'agency': '0001', 'account': '000000001', 'bank': 'nome do banco',
                     'customer_uuid': 'ec72ab8c-c0e7-4a58-b08a-17cd8bbc3823'}
    return {'dict': dict_response, 'object': BankDataCreatePayload(**dict_response)}


@pytest.fixture
def customer_payload():
    dict_response = {'company_name': 'Razao Social', 'billing': 10000.5, 'phone_number': '11 97967-0475',
                     'address': 'Rua lalalend, 123'}
    return {'dict': dict_response, 'object': CustomersPayload(**dict_response)}
