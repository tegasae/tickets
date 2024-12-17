from __future__ import annotations
import abc

from src.adapters import repository
from src.viewers.tickets import AbstractTicketViewer


class AbstractUnitOfWork(abc.ABC):
    users: repository.AbstractRepositoryUser
    tickets: repository.AbstractRepositoryTicket
    view_tickets: AbstractTicketViewer
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    #def collect_new_events(self):
    #    for user in self.users.seen_users:
    #        while product.events:
    #            yield product.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
