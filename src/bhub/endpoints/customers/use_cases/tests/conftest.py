import pytest

from unittest.mock import AsyncMock

from bhub.endpoints.customers.use_cases.customers_create import CustomersCreateUseCase
from bhub.endpoints.customers.use_cases.customers_delete_by_uuid import CustomersDeleteByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_get_by_uuid import CustomersGetByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_update_by_uuid import CustomersUpdateByUuidUseCase


@pytest.fixture
def customers_create_use_case():
    return CustomersCreateUseCase(customers_service=AsyncMock(), logger=AsyncMock())


@pytest.fixture
def customers_delete_by_uuid_use_case():
    return CustomersDeleteByUuidUseCase(customers_service=AsyncMock(), logger=AsyncMock())


@pytest.fixture
def customers_get_by_uuid_use_case():
    return CustomersGetByUuidUseCase(customers_service=AsyncMock(), logger=AsyncMock())


@pytest.fixture
def customers_update_by_uuid_use_case():
    return CustomersUpdateByUuidUseCase(customers_service=AsyncMock(), logger=AsyncMock())
