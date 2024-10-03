import abc

from src.domain.ticket import Client


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, client: Client):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, client_id) -> Client:
        raise NotImplementedError
