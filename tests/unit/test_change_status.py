import pytest

from src.domain.exceptions import InvalidStatus
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed, TicketStatusCancelledOperator, \
    TicketStatusCancelledUser, TicketStatusExecuted
from src.domain.ticket import Ticket


def test_status_accept_to_confirm():
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="The ticket is accepted")
    ticket.status_to_confirmed()
    assert isinstance(ticket.active_status, TicketStatusConfirmed)


def test_status_accept_to_executed():
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="The ticket is accepted")
    with pytest.raises(InvalidStatus):
        ticket.status_to_executed()


def test_status_accept_to_cancel_operator():
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="The ticket is accepted")
    ticket.status_to_cancelled_operator(comment="123")
    assert isinstance(ticket.active_status, TicketStatusCancelledOperator)


def test_status_accept_to_cancel_user():
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="The ticket is accepted")
    ticket.status_to_cancelled_user(comment="123")
    assert isinstance(ticket.active_status, TicketStatusCancelledUser)



def test_status_confirm_to_confirm():
    ticket_status = TicketStatusConfirmed()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="")
    with pytest.raises(InvalidStatus):
        ticket.status_to_confirmed()


def test_ticket_status_confirm_to_execute():
    ticket_status = TicketStatusConfirmed()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    ticket.status_to_executed()
    assert isinstance(ticket.active_status, TicketStatusExecuted)


def test_ticket_status_confirm_to_cancel_operator():
    ticket_status = TicketStatusConfirmed()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    ticket.status_to_cancelled_operator(comment="123")
    assert isinstance(ticket.active_status, TicketStatusCancelledOperator)


def test_ticket_status_confirm_to_cancel_user():
    ticket_status = TicketStatusConfirmed()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    ticket.status_to_cancelled_operator(comment="123")
    assert isinstance(ticket.active_status, TicketStatusCancelledUser)


def test_ticket_status_execute_to_confirm():
    ticket_status = TicketStatusExecuted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    with pytest.raises(InvalidStatus):
        ticket.status_to_confirmed()


def test_ticket_status_execute_to_cancel_operator():
    ticket_status = TicketStatusExecuted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    with pytest.raises(InvalidStatus):
        ticket.status_to_cancelled_operator(comment="123")


def test_ticket_status_execute_to_cancel_user():
    ticket_status = TicketStatusExecuted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    with pytest.raises(InvalidStatus):
        ticket.status_to_cancelled_user(comment="123")

