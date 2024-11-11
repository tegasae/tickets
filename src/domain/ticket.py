from typing import List

from src.domain.exceptions import InvalidStatus, InvalidTicket
from src.domain.status import TicketStatus, TicketStatusConfirmed, TicketStatusExecuted, TicketStatusCancelledUser, \
    TicketStatusAccepted, TicketStatusCancelledOperator, UserStatus, ClientStatus, ClientStatusEnabled, \
    UserStatusEnabled


class Client:
    """Класс клиент"""

    def __init__(self, client_id: int, name: str, status: ClientStatus):
        self.client_id = client_id
        self.name = name
        self.status = status

    def is_active(self):
        if type(self.status) is ClientStatusEnabled:
            return True
        else:
            return False


class Ticket:
    """Класс заявка"""

    def __init__(self, ticket_id: int, describe: str, statuses: List[TicketStatus]):
        """Иницилизация. Если список статусов пуст, то создается статус Принято"""
        self.ticket_id = ticket_id
        if type(describe) is not str or len(describe.lstrip()) == 0:
            raise InvalidTicket()

        self.describe = describe
        self.statuses = []
        if not statuses:
            self.statuses.append(TicketStatusAccepted())
        else:
            self.statuses = statuses

    def __hash__(self):
        return hash(self.ticket_id)

    @property
    def active_status(self):
        """Возврщаем самый последний статус"""
        return self.statuses[-1]

    def status_to_confirmed(self):
        """Перевод заявки в Подтверждено"""
        if type(self.active_status) is TicketStatusAccepted:
            self.statuses.append(TicketStatusConfirmed())
        else:
            raise InvalidStatus()

    def status_to_executed(self):
        """Перевод заяаки в Выполнено"""
        if type(self.active_status)==TicketStatusConfirmed or type(self.active_status)==TicketStatusCancelledUser:
            self.statuses.append(TicketStatusExecuted())
        else:
            raise InvalidStatus()

    def status_to_cancelled_user(self,comment:str):
        """Перевод заявки в снято пользователем"""
        if type(self.active_status) is TicketStatusAccepted or type(self.active_status) is TicketStatusConfirmed:
            self.statuses.append(TicketStatusCancelledUser(comment=comment))
        else:
            raise InvalidStatus()

    def status_to_cancelled_operator(self,comment:str):
        """Перевод заявки в снято оператором"""
        if type(self.active_status) is TicketStatusAccepted or type(self.active_status) is TicketStatusConfirmed:
            self.statuses.append(TicketStatusCancelledOperator(comment=comment))
        else:
            raise InvalidStatus()


class User:
    """Класс пользователь. Может создавать заявки и отменять их"""

    def __init__(self, user_id: int, name: str, client: Client, tickets: List[Ticket], status: UserStatus):
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
        if self.is_active():
            self.tickets[ticket.ticket_id] = ticket

    def cancel_ticket(self, ticket_id: int):
        if ticket_id in self.tickets:
            self.tickets[ticket_id].status_to_cancelled_user()
