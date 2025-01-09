import abc

from src.viewers.data import TicketView, ListTicketView


class AbstractTicketViewer(abc.ABC):
    @abc.abstractmethod
    def get_all_tickets_user(self, user_id:int)->ListTicketView:
        raise NotImplementedError

    @abc.abstractmethod
    def get_ticket(self, user_id: int, ticket_id:int) -> TicketView:
        raise NotImplementedError
