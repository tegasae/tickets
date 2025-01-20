# pylint: disable=too-few-public-methods
import datetime

from dataclasses import dataclass
from typing import Union

from src.domain.client import Client
from src.domain.ticket import Ticket


@dataclass
class Message:
    date: datetime = datetime.datetime.now()
    describe = "The message"


class Command:
    describe = "command"


@dataclass
class CreateTicket(Command):
    user_id: int
    describe: str


@dataclass
class CancelTicket(Command):
    user_id: int
    ticket_id: int
    comment: str


@dataclass(kw_only=True)
class Event(Message):
    describe = "The event"


@dataclass(kw_only=True)
class CreatedTicket(Event):
    ticket: Ticket
    date_created: datetime


@dataclass(kw_only=True)
class CancelledUser(Event):
    user_id: int
    ticket_id: int
    date_cancelled: datetime


@dataclass(kw_only=True)
class ClientEvent(Event):
    describe = "This is the client event"
    client: Client


@dataclass(kw_only=True)
class CreatedClient(ClientEvent):
    describe = "The client is created"


@dataclass(kw_only=True)
class CantCreatedClient(ClientEvent):
    describe = "The client isn't created"
    name: str


@dataclass(kw_only=True)
class AlreadyExitedClient(ClientEvent):
    describe = "The client already exists"
    name: str


@dataclass(kw_only=True)
class CantStoredClient(ClientEvent):
    describe = "The client can't store"


@dataclass(kw_only=True)
class DeletedClient(ClientEvent):
    describe = "The client is deleted"


@dataclass(kw_only=True)
class NotDeletedClient(ClientEvent):
    describe = "The client isn't deleted"

@dataclass(kw_only=True)
class ClientNotFound:
    describe = "The client doesn't find"

ClientEvents = Union[
    CreatedClient, CantCreatedClient, AlreadyExitedClient, CantStoredClient, DeletedClient, NotDeletedClient]
