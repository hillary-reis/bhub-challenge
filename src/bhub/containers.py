from dependency_injector import containers, providers

from bhub.endpoints.bank_data.use_cases.bank_data_create import BankDataCreateUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_delete_by_uuid import BankDataDeleteByUuidUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_get_by_uuid import BankDataGetByUuidUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_update_by_uuid import BankDataUpdateByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_create import CustomersCreateUseCase
from bhub.endpoints.customers.use_cases.customers_delete_by_uuid import CustomersDeleteByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_get_by_uuid import CustomersGetByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_update_by_uuid import CustomersUpdateByUuidUseCase
from bhub.infrastructure.database.sql import PostgresDatabase
from bhub.logger import Logger
from bhub.repositories.bank_data_repository import BankDataSqlRepository
from bhub.repositories.customers_repository import CustomersSqlRepository
from bhub.services.bank_data_service import BankDataService
from bhub.services.customers_service import CustomersService
from config import Config


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(Logger)

    postgres_database = providers.Singleton(PostgresDatabase, db_url=Config.ASYNC_POSTGRES_DATABASE_URL,
                                            logger=logger)

    # repositories
    bank_data_sql_repository = providers.Factory(BankDataSqlRepository,
                                                 session_factory=postgres_database.provided.session, logger=logger)

    customers_sql_repository = providers.Factory(CustomersSqlRepository,
                                                 session_factory=postgres_database.provided.session, logger=logger)

    # services
    bank_data_service = providers.Factory(BankDataService, bank_data_sql_repository=bank_data_sql_repository,
                                          logger=logger)

    customers_service = providers.Factory(CustomersService, customers_sql_repository=customers_sql_repository,
                                          logger=logger)

    # use cases
    bank_data_create_use_case = providers.Factory(BankDataCreateUseCase, bank_data_service=bank_data_service,
                                                  customers_service=customers_service, logger=logger)

    bank_data_delete_by_uuid_use_case = providers.Factory(BankDataDeleteByUuidUseCase,
                                                          bank_data_service=bank_data_service, logger=logger)

    bank_data_get_by_uuid_use_case = providers.Factory(BankDataGetByUuidUseCase, bank_data_service=bank_data_service,
                                                       logger=logger)

    bank_data_update_by_uuid_use_case = providers.Factory(BankDataUpdateByUuidUseCase,
                                                          bank_data_service=bank_data_service, logger=logger)

    customers_create_use_case = providers.Factory(CustomersCreateUseCase, customers_service=customers_service,
                                                  logger=logger)

    customers_delete_by_uuid_use_case = providers.Factory(CustomersDeleteByUuidUseCase,
                                                          customers_service=customers_service, logger=logger)

    customers_get_by_uuid_use_case = providers.Factory(CustomersGetByUuidUseCase, customers_service=customers_service,
                                                       logger=logger)

    customers_update_by_uuid_use_case = providers.Factory(CustomersUpdateByUuidUseCase,
                                                          customers_service=customers_service, logger=logger)
