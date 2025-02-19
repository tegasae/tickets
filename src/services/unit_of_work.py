from __future__ import annotations
import abc

from src.adapters import repository
from src.domain.client import ClientCollection
from src.domain.messages import Message
from src.viewers.clients import AbstractClientViewer
from src.viewers.tickets import AbstractTicketViewer


class AbstractUnitOfWork(abc.ABC):
    users: repository.AbstractRepositoryUser
    tickets: repository.AbstractRepositoryTicket
    client_collection_repository: repository.AbstractRepositoryClientCollection
    view_tickets: AbstractTicketViewer
    view_clients: AbstractClientViewer


    def __init__(self):
        self.client_collect=ClientCollection()
        self.events:list[Message]=[]
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):

        self.rollback()

    def commit(self):
        print("commit")
        for event in self.events:
            print(f"Publishing event: {event}")
        self.events.clear()
        self._commit()
        # Simulate publishing events

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
