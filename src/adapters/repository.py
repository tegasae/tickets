import abc

from src.domain.status import TicketStatus, TicketStatusAccepted, TicketStatusConfirmed, TicketStatusExecuted, \
    TicketStatusCancelledUser, TicketStatusCancelledOperator
from src.domain.ticket import User, Ticket, Client


class AbstractRepositoryClient(abc.ABC):
    def __init__(self):
        self.seen_clients: dict[int, Client] = {}

    def save(self, client:Client) -> Client:
        client = self._save(client=client)
        if client.client_id:
            self.seen_clients[client.client_id] = client
        return client

    def get(self, client_id: int) -> Client:
        client = self._get(client_id=client_id)

        if client.client_id:
            self.seen_clients[client_id] = client
        return client

    def delete(self, client_id: int)->bool:
        if not self._delete(client_id):
            return False
        if client_id in self.seen_clients:
            del (self.seen_clients[client_id])
        return True

    @abc.abstractmethod
    def _save(self, client: Client) -> Client:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, client_id: int) -> Client:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, client_id: int) -> bool:
        raise NotImplementedError



class AbstractRepositoryUser(abc.ABC):
    def __init__(self):
        self.seen_users: dict[int, User] = {}

    def save(self, user: User) -> User:
        user = self._save(user=user)
        if user.user_id:
            self.seen_users[user.user_id] = user
        return user

    def get(self, user_id: int) -> User:
        user = self._get(user_id=user_id)

        if user.user_id:
            self.seen_users[user_id] = user
        return user




    def delete(self, user_id: int):
        if not self._delete(user_id):
            return False
        if user_id in self.seen_users:
            del (self.seen_users[user_id])
        return True

    @abc.abstractmethod
    def _save(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, user_id: int) -> bool:
        raise NotImplementedError




class AbstractRepositoryTicket(abc.ABC):
    def __init__(self):
        self.seen_tickets: dict[int, Ticket] = {}

    def save(self, user_id: int, ticket: Ticket) -> Ticket:
        ticket = self._save(user_id, ticket)
        if ticket.ticket_id != 0:
            self.seen_tickets[ticket.ticket_id] = ticket
        return ticket

    def get(self, user_id: int) -> list[Ticket]:
        tickets = self._get(user_id)
        for t in tickets:
            self.seen_tickets[t.ticket_id] = t
        return tickets

    def delete(self, user_id: int, ticket_id: int) -> bool:
        if not self._delete(user_id=user_id, ticket_id=ticket_id):
            return False

        if ticket_id in self.seen_tickets:
            del (self.seen_tickets[ticket_id])
        return True

    @abc.abstractmethod
    def _save(self, user_id: int, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_id: int) -> list[Ticket]:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, user_id: int, ticket_id: int) -> bool:
        raise NotImplemented


class _RepositoryStatus:
    TicketStatusId = {
        0: TicketStatus,
        1: TicketStatusAccepted,
        2: TicketStatusConfirmed,
        3: TicketStatusExecuted,
        4: TicketStatusCancelledUser,
        5: TicketStatusCancelledOperator
    }

    @staticmethod
    def get_status_by_id(status_id: int) -> type(TicketStatus):
        return _RepositoryStatus.TicketStatusId.get(status_id, TicketStatus)

    @staticmethod
    def get_id_by_status(status) -> int:
        for s in _RepositoryStatus.TicketStatusId:
            if type(status) is _RepositoryStatus.TicketStatusId[s]:
                return s
        return 0
