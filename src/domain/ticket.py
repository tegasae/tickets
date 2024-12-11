from typing import List

from src.domain.exceptions import InvalidStatus, InvalidTicket, CommentNotFill
from src.domain.status import TicketStatus, TicketStatusConfirmed, TicketStatusCancelledUser, \
    TicketStatusAccepted, UserStatus, ClientStatus, ClientStatusEnabled, \
    UserStatusEnabled


class Client:
    """Класс клиент"""

    def __init__(self, client_id: int, name: str, status: ClientStatus):
        self.client_id = client_id
        self.name = name
        self.status = status
        self.events=[]

    def is_active(self):
        if type(self.status) is ClientStatusEnabled:
            return True
        else:
            return False


class Ticket:
    """Класс заявка"""

    def __init__(self, ticket_id: int = 0, describe: str = "", statuses: List[TicketStatus] | None = None):
        """Иницилизация. Если список статусов пуст, то создается статус Принято"""
        self.ticket_id = ticket_id
        if type(describe) is not str or len(describe.lstrip()) == 0:
            raise InvalidTicket()

        self.describe = describe
        self.statuses = []
        if statuses is None or not statuses:
            self.statuses.append(TicketStatusAccepted())
        else:
            self.statuses = statuses

        self.events=[]

    def __hash__(self):
        return hash(self.ticket_id)

    def __eq__(self, other):
        if self.ticket_id == other.ticket_id:
            return True
        else:
            return False

    @property
    def date_created(self):
        return self.statuses[0].date

    @property
    def active_status(self):
        """Возврщаем самый последний статус"""
        return self.statuses[-1]

    def cancelled_by_user(self, comment: str):
        """Перевод заявки в снято пользователем"""
        if comment=="":
            raise CommentNotFill()
        if type(self.active_status) is TicketStatusAccepted or type(self.active_status) is TicketStatusConfirmed:
            self.statuses.append(TicketStatusCancelledUser(comment=comment))
        else:
            raise InvalidStatus()


class User:
    """Класс пользователь. Может создавать заявки и отменять их"""

    def __init__(self, user_id: int, name: str, client: Client, status: UserStatus, tickets: list[Ticket] = None):
        self.user_id = user_id
        self.name = name
        self.client = client
        self.tickets = {}
        if tickets:
            for t in tickets:
                self.tickets[t.ticket_id] = t

        self.status = status

    def is_active(self):
        if self.client.is_active() and type(self.status) is UserStatusEnabled:
            return True
        else:
            return False

    def create_ticket(self, ticket: Ticket):
        active=self.is_active()
        if active==True:
            self.tickets[ticket.ticket_id] = ticket

    def cancel_ticket(self, ticket_id: int, comment: str) -> Ticket:

        if ticket_id in self.tickets:
            self.tickets[ticket_id].cancelled_by_user(comment=comment)
            return self.tickets[ticket_id]
        return Ticket(ticket_id=0, describe="1")
