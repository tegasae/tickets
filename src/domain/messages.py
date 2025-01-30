# pylint: disable=too-few-public-methods
import datetime

from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True)
class Message:
    date: datetime = field(default_factory=datetime.datetime.now)
    describe = "The message"


@dataclass(kw_only=True, frozen=True)
class Command(Message):
    describe = "command"


@dataclass(kw_only=True, frozen=True)
class Event(Message):
    describe = "event"


@dataclass(kw_only=True, frozen=True)
class EventClient(Event):
    describe = "client event"


@dataclass(kw_only=True, frozen=True)
class EventClientCreated(EventClient):
    describe = "client created"
    client_id: int = 0


@dataclass(kw_only=True, frozen=True)
class EventClientUpdated(EventClient):
    describe = "client created"
    client_id: int

@dataclass(kw_only=True, frozen=True)
class EventClientAlreadyExists(EventClient):
    describe = "client exists"
    client_id: int


@dataclass(kw_only=True, frozen=True)
class EventClientWronged(EventClient):
    describe = "client wrong"
    client_id:int
    name: str


@dataclass(kw_only=True, frozen=True)
class EventClientDeleted(EventClient):
    describe = "client deleted"


@dataclass(kw_only=True, frozen=True)
class EventClientCantDeleted(EventClient):
    describe = "client can't deleted"
