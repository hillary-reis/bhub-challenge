from pydantic import BaseModel, validator, Field
from typing import Optional


class BankDataPayload(BaseModel):
    agency: str = Field(max_length=5)
    account: str = Field(max_length=9)
    bank: str = Field(max_length=50)

    def __init_subclass__(cls, optional_fields=(), **kwargs):
        super().__init_subclass__(**kwargs)
        for field in optional_fields:
            cls.__fields__[field].outer_type_ = Optional
            cls.__fields__[field].required = False


class BankDataCreatePayload(BankDataPayload):
    customer_uuid: str


_patch_fields_bank_data = BankDataPayload.__fields__.keys()


class BankDataUpdatePayload(BankDataPayload, optional_fields=_patch_fields_bank_data):
    pass


class BankDataResponse(BaseModel):
    uuid: str
    created_at: str
    agency: str
    account: str
    bank: str
    customer_uuid: str

    @validator('created_at', pre=True)
    def convert_datetime_to_str(cls, created_at):
        return created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    class Config:
        orm_mode = True


class BankDataCreateResponse(BankDataResponse):
    pass


