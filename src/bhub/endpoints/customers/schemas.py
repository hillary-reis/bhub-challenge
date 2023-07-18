import re

from pydantic import BaseModel, condecimal, validator
from typing import Optional


class CustomersPayload(BaseModel):
    company_name: str
    phone_number: str
    address: str
    billing: condecimal(decimal_places=2)

    def __init_subclass__(cls, optional_fields=(), **kwargs):
        super().__init_subclass__(**kwargs)
        for field in optional_fields:
            cls.__fields__[field].outer_type_ = Optional
            cls.__fields__[field].required = False

    @validator('phone_number')
    def validate_phone_number(cls, phone_number) -> str | None:
        phone_number = re.sub('[^\\d+]', '', phone_number)
        phone_pattern = r'^(?:\+55)?\(?0?[1-9][1-9]\)?\s?(?:9)?\s?\d{4}\-?\d{4,5}$'

        if not re.match(phone_pattern, phone_number):
            raise ValueError('The phone number provided seems to be not in a valid format')

        if not phone_number.startswith('+55'):
            phone_number = f'+55{phone_number}'

        return phone_number

    @validator('billing')
    def convert_decimal_to_int(cls, billing):
        return int(billing * 100)


class CustomersCreatePayload(CustomersPayload):
    pass

class CustomerResponse(BaseModel):
    uuid: str
    created_at: str
    company_name: str
    phone_number: str
    address: str
    billing: float

    @validator('billing', pre=True)
    def convert_int_to_float(cls, billing):
        return round(float(billing / 100), 2)

    @validator('created_at', pre=True)
    def convert_datetime_to_str(cls, created_at):
        return created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    class Config:
        orm_mode = True


class CustomersCreateResponse(CustomerResponse):
    pass


class CustomersGetByUuidResponse(CustomerResponse):
    pass
