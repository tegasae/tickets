from dataclasses import dataclass
from datetime import datetime

from src.domain.exceptions import InvalidStatus
from src.domain.status import TicketStatus, TicketStatusConfirmed, TicketStatusExecuted, TicketStatusCancelledUser


@dataclass
class Client:
    client_id:int
    name: str

class Ticket:
    ticket_id:int
    client:Client
    date_create: datetime
    date_executed: datetime
    status: TicketStatus
    describe: str
    comment: str

    def status_to_executed(self):
        if type(self.status)==TicketStatusConfirmed:
            self.status=TicketStatusExecuted()
            return
        raise InvalidStatus()

