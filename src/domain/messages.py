# pylint: disable=too-few-public-methods
import datetime

from dataclasses import dataclass



@dataclass(kw_only=True)
class Message:
    date: datetime = datetime.datetime.now()
    describe = "The message"


@dataclass(kw_only=True)
class Command(Message):
    describe = "command"


@dataclass(kw_only=True)
class Event(Message):
    describe = "event"

@dataclass(kw_only=True)
class EventClient(Event):
    describe = "client event"

@dataclass(kw_only=True)
class EventClientCreated(EventClient):
    describe = "client created"
    client_id:int=0

@dataclass(kw_only=True)
class EventClientUpdated(EventClient):
    describe = "client created"
    client_id:int=0


@dataclass(kw_only=True)
class EventClientAlreadyExists(EventClient):
    describe = "client exists"
    client_id:int=0

@dataclass(kw_only=True)
class EventClientWronged(EventClient):
    describe = "client wrong"
    name:str=""


@dataclass(kw_only=True)
class EventClientDeleted(EventClient):
    describe = "client deleted"


@dataclass(kw_only=True)
class EventClientCantDeleted(EventClient):
    describe = "client can't deleted"








