import pytest
from unittest.mock import MagicMock

from bhub.repositories.bank_data_repository import BankDataSqlRepository
from bhub.repositories.customers_repository import CustomersSqlRepository
from bhub.services.bank_data_service import BankDataService
from bhub.services.customers_service import CustomersService


@pytest.fixture
def bank_data_sql_repository_mock():
    bank_data = MagicMock(spec=BankDataSqlRepository)
    yield bank_data


@pytest.fixture
def customers_sql_repository_mock():
    customers = MagicMock(spec=CustomersSqlRepository)
    yield customers


@pytest.fixture
def bank_data_service(bank_data_sql_repository_mock):
    return BankDataService(bank_data_sql_repository=bank_data_sql_repository_mock, logger=MagicMock())


@pytest.fixture
def customers_service(customers_sql_repository_mock):
    return CustomersService(customers_sql_repository=customers_sql_repository_mock, logger=MagicMock())
