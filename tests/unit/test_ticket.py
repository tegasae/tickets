import pytest

from src.domain.exceptions import InvalidTicket
from src.domain.ticket import Client, Ticket
from src.domain.status import ClientStatusEnabled, ClientStatusDisabled, TicketStatusAccepted


def test_create_empty_ticket():
    with pytest.raises(InvalidTicket):
        ticket = Ticket(123, "", [])


def test_create_space_ticket():
    with pytest.raises(InvalidTicket):
        ticket = Ticket(123, "      ", [])


def test_client_is_active_enabled():
    client = Client(1, "Test Client", ClientStatusEnabled())
    assert client.is_active() == True


def test_client_is_active_disabled():
    client = Client(2, "Test Client", ClientStatusDisabled())
    assert client.is_active() == False


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
