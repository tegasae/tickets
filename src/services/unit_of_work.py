from __future__ import annotations
import abc

from src.adapters import repository
from src.domain.client import ClientsCollect
from src.domain.messages import Message
from src.viewers.clients import AbstractClientViewer
from src.viewers.tickets import AbstractTicketViewer


class AbstractUnitOfWork(abc.ABC):
    users: repository.AbstractRepositoryUser
    tickets: repository.AbstractRepositoryTicket
    clients: repository.AbstractRepositoryClient
    view_tickets: AbstractTicketViewer
    view_clients: AbstractClientViewer
    client_collect: ClientsCollect

    def __init__(self):
        self.client_collect=ClientsCollect()
        self.events:list[Message]=[]
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        print("commit")
        self._commit()

    # def collect_new_events(self):
    #    for user in self.users.seen_users:
    #        while product.events:
    #            yield product.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        print("rollback")
        raise NotImplementedError
