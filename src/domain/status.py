from dataclasses import dataclass, field, asdict
from datetime import datetime

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
    id=0
    name: str = "Ticket status"
    date: datetime = field(default_factory=datetime.now)
    comment: str = ""


@dataclass(frozen=True, kw_only=True)
class TicketStatusAccepted(TicketStatus):
    """Заявка принята"""
    id=1
    name: str = "Accepted"


@dataclass(frozen=True)
class TicketStatusConfirmed(TicketStatus):
    """Заявка подтверждена оператором"""
    id=2
    name: str = "Confirmed by an operator"


@dataclass(frozen=True)
class TicketStatusExecuted(TicketStatus):
    """Заявка выполнена"""
    id=3
    name: str = "Executed"


@dataclass(frozen=True, kw_only=True)
class TicketStatusCancelledUser(TicketStatus):
    """Заявка снята пользователем"""
    id=4
    name: str = "Cancelled by an user"
    comment: str


@dataclass(frozen=True, kw_only=True)
class TicketStatusCancelledOperator(TicketStatus):
    """Заявка снята оператором"""
    id=5
    name: str = "Cancelled by an operator"
    comment: str



def get_status_by_id(status_id:int)->type(TicketStatus):
    if status_id==0:
        return TicketStatus
    if status_id==1:
        return TicketStatusAccepted
    if status_id==2:
        return TicketStatusConfirmed
    if status_id==3:
        return TicketStatusExecuted
    if status_id==4:
        return TicketStatusCancelledUser
    if status_id==5:
        return TicketStatusCancelledOperator

def get_id_by_status(status:TicketStatus)->int:
    return status.id

"""Статусы клиентов"""


@dataclass
class ClientStatus:
    """Базовый класс статусов клиента"""
    id:int=0
    name: str = field(default="This is the client status")
    #date: datetime = field(default_factory=datetime.now)
    def enabled(self)->bool:
        if self.id==1:
            return True
        else:
            return False

    def __repr__(self):
        return repr(asdict(self))

@dataclass
class ClientStatusEnabled(ClientStatus):
    """Клиент вклдючен"""
    id:int = 1
    name: str = field(default="The client is enabled")

@dataclass
class ClientStatusDisabled(ClientStatus):
    """Клиент отключен"""
    id:int = 2
    name: str = field(default="The client is disabled")

_list_of_status=(ClientStatus,ClientStatusEnabled,ClientStatusDisabled)

class ClientStatusOperation:
    @staticmethod
    def by_id(status_id:int)->ClientStatus:
        for i in _list_of_status:
            if i.id==status_id:
                return i()

        return _list_of_status[0]()

    @staticmethod
    def by_type(client_status_type:type(ClientStatus))->int:
        for cst in _list_of_status:
            if client_status_type is cst:
                return cst.id
        return _list_of_status[0].id

    @staticmethod
    def by_enable(enable:bool)->ClientStatus:
        if enable:
            return ClientStatusEnabled()
        else:
            return ClientStatusDisabled()
    #@staticmethod
    #def by_name(client_status_name:str):
    #    for csn in _list_of_status:
    #        if csn.name