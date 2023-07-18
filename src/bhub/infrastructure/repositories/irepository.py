import abc

from bhub.logger import Logger


class IRepository(metaclass=abc.ABCMeta):
    def __init__(self, session_factory, logger: Logger) -> None:
        self.session_factory = session_factory
        self.logger = logger
