# pylint: disable=too-few-public-methods
import datetime
from datetime import date
from typing import Optional
from dataclasses import dataclass


class Command:
    describe="command"


@dataclass
class CreateTicket(Command):
    user_id: int
    describe: str


@dataclass
class CancelTicket(Command):
    user_id: int
    ticket_id: int
    comment: str

class Event:
    describe="event"

@dataclass
class Created(Event):
    user_id: int
    ticket_id: int
    date_created: datetime

@dataclass
class CancelledUser(Event):
    user_id: int
    ticket_id: int
    date_cancelled: datetime

