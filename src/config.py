from os import getenv
from distutils.util import strtobool


class Config:
    APP_ENV = getenv('APP_ENV', 'local')
    LOG_LEVEL = getenv('LOG_LEVEL', 'DEBUG')
    SERVER_PORT = int(getenv('SERVER_PORT', '8080'))

    ASYNC_POSTGRES_DATABASE_URL = getenv('ASYNC_POSTGRES_DATABASE_URL',
                                         'postgresql+asyncpg://bhub:bhub@localhost:5432/bhub')
    SQL_ECHO = bool(strtobool(getenv('SQL_ECHO', 'False')))
    SQL_POOL_SIZE = getenv('SQL_POOL_SIZE', 5)
    SQL_MAX_OVERFLOW = getenv('SQL_MAX_OVERFLOW', 10)
