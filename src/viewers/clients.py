import abc

from src.viewers.data import ClientView


class AbstractClientViewer(abc.ABC):

    @abc.abstractmethod
    def get_client(self, client_id: int) -> ClientView:
        raise NotImplementedError

    @abc.abstractmethod
    def get_client_by_name(self, name: str) -> list[ClientView]:
        raise NotImplementedError


    @abc.abstractmethod
    def get_all_clients(self)->list[ClientView]:
        raise NotImplementedError

