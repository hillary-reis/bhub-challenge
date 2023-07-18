import pytest

from unittest.mock import AsyncMock

from bhub.endpoints.bank_data.use_cases.bank_data_create import BankDataCreateUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_delete_by_uuid import BankDataDeleteByUuidUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_get_by_uuid import BankDataGetByUuidUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_update_by_uuid import BankDataUpdateByUuidUseCase


@pytest.fixture
def bank_data_create_use_case():
    return BankDataCreateUseCase(bank_data_service=AsyncMock(), customers_service=AsyncMock(), logger=AsyncMock())


@pytest.fixture
def bank_data_delete_by_uuid_use_case():
    return BankDataDeleteByUuidUseCase(bank_data_service=AsyncMock(), logger=AsyncMock())


@pytest.fixture
def bank_data_get_by_uuid_use_case():
    return BankDataGetByUuidUseCase(bank_data_service=AsyncMock(), logger=AsyncMock())


@pytest.fixture
def bank_data_update_by_uuid_use_case():
    return BankDataUpdateByUuidUseCase(bank_data_service=AsyncMock(), logger=AsyncMock())
