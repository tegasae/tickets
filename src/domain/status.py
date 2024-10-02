from dataclasses import dataclass, field
from datetime import datetime

"""Модуль определяющий статусы клиента, пользователя и заявки"""

"""Классы статусов пользователя"""
@dataclass(frozen=True)
class UserStatus:
    """Базовый класс для статуса пользователя"""
    name:str= field(default="User status")
    date: datetime = field(default_factory=datetime.now)

@dataclass(frozen=True)
class UserStatusEnabled(UserStatus):
    """Пользователь включен"""
    name: str = field(default="Enable")


@dataclass(frozen=True)
class UserStatusDisabled(UserStatus):
    """Пользоввтеь отключен"""
    name: str = field(default="Disable")


"""Классы статусов заявки"""
@dataclass(frozen=True)
class TicketStatus:
    """Базовый класс статусов заявок"""
    name: str = field(default="Ticket status")
    date: datetime = field(default_factory=datetime.now)

@dataclass(frozen=True)
class TicketStatusAccepted(TicketStatus):
    """Заявка принята"""
    name: str = field(default="Accepted")


@dataclass(frozen=True)
class TicketStatusConfirmed(TicketStatus):
    """Заявка подтверждена оператором"""
    name: str = field(default="Confirmed by an operator")


@dataclass(frozen=True)
class TicketStatusExecuted(TicketStatus):
    """Заявка выполнена"""
    name: str = field(default="Executed")


@dataclass(frozen=True)
class TicketStatusCancelledUser(TicketStatus):
    """Заявка снята пользователем"""
    name: str = field(default="Cancelled by an user")



@dataclass(frozen=True)
class TicketStatusCancelledOperator(TicketStatus):
    """Заявка снята оператором"""
    name: str = field(default="Cancelled by an operator")

"""Статусы клиентов"""
@dataclass
class ClientStatus:
    """Базовый класс статусов клиента"""
    name:str=field(default="This is the client status")
    date: datetime = field(default_factory=datetime.now)



@dataclass
class ClientStatusEnabled(ClientStatus):
    """Клиент вклдючен"""
    name:str=field(default="The client is enabled")



@dataclass
class ClientStatusDisabled(ClientStatus):
    """Клиент отключен"""
    name: str = field(default="The client is disabled")

