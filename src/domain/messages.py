# pylint: disable=too-few-public-methods
import datetime
from datetime import date
from typing import Optional
from dataclasses import dataclass

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
    ticket:Ticket
    date_created: datetime

@dataclass(kw_only=True)
class CancelledUser(Event):
    user_id: int
    ticket_id: int
    date_cancelled: datetime


