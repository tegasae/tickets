from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Type

"""Модуль определяющий статусы клиента, пользователя и заявки"""

"""Классы статусов пользователя"""


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


"""Классы статусов заявки"""


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


def get_status_by_id(status_id: int) -> type(TicketStatus):
    if status_id == 0:
        return TicketStatus
    if status_id == 1:
        return TicketStatusAccepted
    if status_id == 2:
        return TicketStatusConfirmed
    if status_id == 3:
        return TicketStatusExecuted
    if status_id == 4:
        return TicketStatusCancelledUser
    if status_id == 5:
        return TicketStatusCancelledOperator


def get_id_by_status(status: TicketStatus) -> int:
    return status.id


"""Статусы клиентов"""



class ClientStatus:
    id = 0


class ClientStatusEnabled(ClientStatus):
    id = 1


class ClientStatusDisabled(ClientStatus):
    id = 2


_list_of_status = (ClientStatus, ClientStatusEnabled, ClientStatusDisabled)


class ClientStatusOperation:
    @staticmethod
    def by_id(status_id: int) -> ClientStatus:
        """Retrieve a ClientStatus instance by its ID."""
        for status in _list_of_status:
            if status.id == status_id:
                return status()
        return _list_of_status[0]()  # Default to the first status

    @staticmethod
    def by_type(client_status_type: Type[ClientStatus]) -> int:
        """Retrieve the ID of a given ClientStatus type."""
        for status in _list_of_status:
            if client_status_type is status:
                return status.id
        return _list_of_status[0].id  # Default to the first status ID

    @staticmethod
    def by_enable(enable: bool) -> ClientStatus:
        """Retrieve ClientStatus based on the enable flag."""
        return ClientStatusEnabled() if enable else ClientStatusDisabled()
