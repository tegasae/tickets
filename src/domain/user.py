from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime

from src.domain.ticket import Ticket


class User:
    """Класс пользователь. Может создавать заявки и отменять их"""

    def __init__(self, user_id: int, name: str, status: UserStatus, tickets: list[Ticket] = None):
        self.user_id = user_id
        self.name = name
        self.tickets = {}
        if tickets:
            for t in tickets:
                self.tickets[t.ticket_id] = t

        self.status = status

    def disabled(self):
        self.status = UserStatusDisabled()

    def enables(self):
        self.status = UserStatusEnabled()

    def is_active(self):
        if isinstance(self.status, UserStatusEnabled):
            return True
        else:
            return False

    def create_ticket(self, ticket: Ticket) -> bool:
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
        return Ticket.empty_ticket()

    @classmethod
    def empty_user(cls):
        return cls(user_id=0, name="", tickets=[], status=UserStatusDisabled())


class UserExceptionIsDisabled(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)  # Initialize the base Exception class


@dataclass(kw_only=True, frozen=True)
class UserStatus:
    """Базовый класс для статуса пользователя"""
    name: str = field(default="User status")
    date: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return repr(asdict(self))


@dataclass(frozen=True)
class UserStatusEnabled(UserStatus):
    """Пользователь включен"""
    name: str = field(default="Enable")


@dataclass(frozen=True)
class UserStatusDisabled(UserStatus):
    """Пользоввтеь отключен"""
    name: str = field(default="Disable")
