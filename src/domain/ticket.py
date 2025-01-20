from typing import List

from src.domain.client import Client
from src.domain.status import TicketStatus, TicketStatusConfirmed, TicketStatusCancelledUser, \
    TicketStatusAccepted, UserStatus, UserStatusEnabled, UserStatusDisabled


class Ticket:
    """Класс заявка"""

    def __init__(self, ticket_id: int = 0, describe: str = "", statuses: List[TicketStatus] | None = None):
        """Иницилизация. Если список статусов пуст, то создается статус Принято"""
        self.ticket_id = ticket_id

        self.describe = describe
        self.statuses = []
        if statuses is None or not statuses:
            self.statuses.append(TicketStatusAccepted())
        else:
            self.statuses = statuses

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

    def cancelled_by_user(self, comment: str) -> bool:
        """Перевод заявки в снято пользователем"""
        if type(self.active_status) is TicketStatusAccepted or type(self.active_status) is TicketStatusConfirmed:
            self.statuses.append(TicketStatusCancelledUser(comment=comment))
            return True
        else:
            return False

    @classmethod
    def empty_ticket(cls):
        return cls(ticket_id=0, describe="", statuses=[])


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

    def create_ticket(self, ticket: Ticket) -> bool:
        if ticket.describe.lstrip() == "":
            return False
        if not self.is_active():
            return False

        self.tickets[ticket.ticket_id] = ticket
        return True

    def add_tickets(self, tickets: list[Ticket]):
        for t in tickets:
            self.create_ticket(t)

    def cancel_ticket(self, ticket_id: int, comment: str) -> Ticket:
        if ticket_id in self.tickets:
            self.tickets[ticket_id].cancelled_by_user(comment=comment)
            return self.tickets[ticket_id]
        return Ticket(ticket_id=0, describe="", statuses=[])

    @classmethod
    def empty_user(cls):
        return cls(user_id=0, name="", client=Client.empty_client(), tickets=[], status=UserStatusDisabled())
