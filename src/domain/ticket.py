from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


class Ticket:
    """Класс заявка"""

    def __init__(self, ticket_id: int = 0, describe: str = "", statuses: List[TicketStatus] | None = None):
        """Иницилизация. Если список статусов пуст, то создается статус Принято"""
        self.ticket_id = ticket_id
        self._describe = ""  # Приватное поле
        self.describe = describe
        self.statuses = []
        if statuses is None or not statuses:
            self.statuses.append(TicketStatusAccepted())
        else:
            self.statuses = statuses

    def __hash__(self):
        return hash(self.ticket_id)

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return False
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

    @property
    def describe(self) -> str:
        return self._describe

    @describe.setter
    def describe(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Описание заявки не может быть пустым")
        self._describe = value.strip()

    @classmethod
    def empty_ticket(cls):
        """Create an empty ticket instance that bypasses normal validation"""
        instance = cls.__new__(cls)
        instance.ticket_id = 0
        instance._describe = ""
        instance.statuses = []
        return instance




@dataclass(frozen=True, kw_only=True)
class TicketStatus:
    """Базовый класс статусов заявок"""
    id = 0
    name: str = "Ticket status"
    date: datetime = field(default_factory=datetime.now)
    comment: str = ""


@dataclass(frozen=True, kw_only=True)
class TicketStatusAccepted(TicketStatus):
    """Заявка принята"""
    id = 1
    name: str = "Accepted"


@dataclass(frozen=True)
class TicketStatusConfirmed(TicketStatus):
    """Заявка подтверждена оператором"""
    id = 2
    name: str = "Confirmed by an operator"


@dataclass(frozen=True)
class TicketStatusExecuted(TicketStatus):
    """Заявка выполнена"""
    id = 3
    name: str = "Executed"


@dataclass(frozen=True, kw_only=True)
class TicketStatusCancelledUser(TicketStatus):
    """Заявка снята пользователем"""
    id = 4
    name: str = "Cancelled by an user"
    comment: str


@dataclass(frozen=True, kw_only=True)
class TicketStatusCancelledOperator(TicketStatus):
    """Заявка снята оператором"""
    id = 5
    name: str = "Cancelled by an operator"
    comment: str


_status_map = {
     TicketStatus.id: TicketStatus,
     TicketStatusAccepted.id: TicketStatusAccepted,
     TicketStatusConfirmed.id:TicketStatusConfirmed,
     TicketStatusExecuted.id:TicketStatusExecuted,
     TicketStatusCancelledUser.id:TicketStatusCancelledUser,
     TicketStatusCancelledOperator.id:TicketStatusCancelledOperator
}

def get_status_by_id(status_id: int) -> type[TicketStatus]:
    return _status_map.get(status_id, TicketStatus)


def get_id_by_status(status: TicketStatus) -> int:
    return status.id
