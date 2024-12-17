import abc

from src.viewers.data import TicketView, ListTicketView


class AbstractTicketViewer(abc.ABC):
    @abc.abstractmethod
    def get_all_tickets(self,user_id:int)->ListTicketView:
        raise NotImplementedError

