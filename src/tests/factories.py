import factory

from faker import Faker
from uuid import uuid4

from bhub.infrastructure.models.bank_data import BankData
from bhub.infrastructure.models.customers import Customers


fake = Faker('pt_BR')


class CustomersFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Customers
        strategy = factory.BUILD_STRATEGY

    id = factory.Sequence(lambda n: n)
    uuid = factory.LazyAttribute(lambda obj: str(uuid4()))
    created_at = factory.LazyAttribute(lambda obj: fake.date_time())
    updated_at = factory.LazyAttribute(lambda obj: fake.date_time())
    billing = factory.LazyAttribute(lambda obj: fake.pyint())
    company_name = factory.LazyAttribute(lambda obj: fake.word())
    phone_number = factory.LazyAttribute(lambda x: fake.phone_number())
    address = factory.LazyAttribute(lambda obj: fake.street_name())


class BankDataFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BankData
        strategy = factory.BUILD_STRATEGY

    id = factory.Sequence(lambda n: n)
    uuid = factory.LazyAttribute(lambda obj: str(uuid4()))
    created_at = factory.LazyAttribute(lambda obj: fake.date_time())
    updated_at = factory.LazyAttribute(lambda obj: fake.date_time())
    agency = str(factory.LazyAttribute(lambda obj: fake.pyint()))
    account = str(factory.LazyAttribute(lambda obj: fake.pyint()))
    bank = factory.LazyAttribute(lambda obj: fake.word())

    customer = factory.SubFactory(CustomersFactory)
    customer_id = factory.SelfAttribute('customer.id')
