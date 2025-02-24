from __future__ import annotations
import abc

from src.adapters import repository
from src.domain.client import ClientCollection
from src.domain.messages import Message, Event
from src.viewers.clients import AbstractClientViewer
from src.viewers.tickets import AbstractTicketViewer


class AbstractUnitOfWork(abc.ABC):
    users: repository.AbstractRepositoryUser
    tickets: repository.AbstractRepositoryTicket
    client_collection: repository.AbstractRepositoryClientCollection
    view_tickets: AbstractTicketViewer
    view_clients: AbstractClientViewer


    def __init__(self):
        self.events:list[Event]=[]

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        print("commit")

        self._commit()
        # Simulate publishing events

    def get_events(self):
        event=self.events[:]
        self.events.clear()
        return event

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        print("rollback")

        raise NotImplementedError
