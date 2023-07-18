import pytest

from bhub.endpoints.customers.schemas import CustomersPayload


@pytest.mark.parametrize('phone_number', ['119999999', '123', 'phone1'])
@pytest.mark.asyncio
async def test_customers_payload_failed_invalid_phone_number(phone_number, customer_payload):
    customer_payload['dict']['phone_number'] = phone_number
    with pytest.raises(ValueError) as e:
        CustomersPayload(**customer_payload['dict'])

    assert str(e.value) == '1 validation error for CustomersPayload\nphone_number\n  The phone number provided seems ' \
                           'to be not in a valid format (type=value_error)'
