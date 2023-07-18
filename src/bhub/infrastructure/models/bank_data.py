import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import force_auto_coercion

from bhub.infrastructure.models.base import Base
from bhub.infrastructure.models.customers import Customers


force_auto_coercion()


class BankData(Base):
    __tablename__ = 'bank_data'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column(String(36), default=lambda x: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    agency = Column(String(5), nullable=False)
    account = Column(String(9), nullable=False)
    bank = Column(String(50), nullable=False)

    customer_id = Column(ForeignKey(Customers.id), index=True)
    customer = relationship(Customers, backref=backref('bank_data', lazy=True))
