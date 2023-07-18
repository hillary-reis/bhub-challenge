import abc


class IDatabase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def session(self):
        pass
