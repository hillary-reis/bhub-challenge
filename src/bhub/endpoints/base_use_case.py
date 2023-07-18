from abc import ABCMeta, abstractmethod


class BaseUseCase(metaclass=ABCMeta):
    @abstractmethod
    def run(self, **kwargs) -> None:
        pass
