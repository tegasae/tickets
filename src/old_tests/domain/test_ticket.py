import datetime

import pytest

from src.domain.exceptions import InvalidTicket, InvalidStatus
from src.domain.ticket import Ticket
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed, \
    TicketStatusExecuted, TicketStatusCancelledUser





def test_ticket_initial_status_default():
    ticket = Ticket(123, "Test Ticket", [])
    assert len(ticket.statuses) == 1
    assert isinstance(ticket.statuses[0], TicketStatusAccepted)


def test_ticket_initial_status_provided():
    statuses = [TicketStatusAccepted()]
    ticket = Ticket(124, "Test Ticket", statuses)
    assert ticket.statuses == statuses


def test_ticket_active_status():
    statuses = [TicketStatusAccepted()]
    ticket = Ticket(125, "Test Ticket", statuses)
    assert ticket.active_status == statuses[-1]


def test_ticket_hash():
    ticket = Ticket(126, "Test Ticket", [])
    assert hash(ticket) == hash(ticket.ticket_id)


def test_get_date():
    ticket = Ticket(126, "Test Ticket", [])
    assert type(ticket.date_created) is datetime.datetime


def test_cancel_ticket():
    ticket = Ticket(126, "Test Ticket", [])
    ticket.statuses.append(TicketStatusConfirmed())
    ticket.cancelled_by_user(comment="comment")
    assert type(ticket.active_status) is TicketStatusCancelledUser


def test_cannot_cancel_ticket():

    ticket = Ticket(126, "Test Ticket", [TicketStatusAccepted(),TicketStatusConfirmed(),TicketStatusExecuted()])
    with pytest.raises(InvalidStatus):
        ticket.cancelled_by_user(comment="comment")


def test_find_ticket_in_list():
    tickets=[Ticket(126, "Test Ticket", [TicketStatusAccepted(),TicketStatusConfirmed(),TicketStatusExecuted()]),
             Ticket(127, "Test Ticket", [TicketStatusAccepted(),TicketStatusConfirmed(),TicketStatusExecuted()]),
             Ticket(150, "Test Ticket", [TicketStatusAccepted(),TicketStatusConfirmed(),TicketStatusExecuted()])]
    t=tickets.index(Ticket(127, "Test Ticket", [TicketStatusAccepted(),TicketStatusConfirmed(),TicketStatusExecuted()]))

    assert tickets[t].ticket_id==127
