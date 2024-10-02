import pytest

from src.domain.exceptions import InvalidStatus
from src.domain.status import UserStatusEnabled, ClientStatusEnabled, ClientStatusDisabled, UserStatusDisabled, \
    TicketStatusAccepted, TicketStatusCancelledUser, TicketStatusConfirmed, TicketStatusExecuted, \
    TicketStatusCancelledOperator
from src.domain.ticket import Client, User, Ticket


# Предполагается, что необходимые классы и исключения импортированы из вашего модуля
# from your_module import User, Ticket, Client, UserStatusEnabled, UserStatusDisabled, \
#     TicketStatusAccepted, TicketStatusConfirmed, TicketStatusCancelledUser, \
#     InvalidStatus

def test_user_is_active():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    assert user.is_active() is True


def test_user_is_inactive_due_to_client():
    client = Client(client_id=1, name="Test Client", status=ClientStatusDisabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    assert user.is_active()  is False


def test_user_is_inactive_due_to_status():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    user_status = UserStatusDisabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    assert user.is_active() is False


def test_user_create_ticket():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    user.create_ticket(ticket)
    assert ticket.ticket_id in user.tickets


def test_user_cannot_create_ticket_when_inactive():
    client = Client(client_id=1, name="Test Client", status=ClientStatusDisabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    user.create_ticket(ticket)
    assert ticket.ticket_id not in user.tickets


def test_user_cancel_ticket():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    user.create_ticket(ticket)
    user.cancel_ticket(ticket_id=1)
    assert isinstance(user.tickets[1].active_status, TicketStatusCancelledUser)


def test_ticket_status_transition_to_confirmed():
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    ticket.status_to_confirmed()
    assert isinstance(ticket.active_status, TicketStatusConfirmed)


def test_ticket_status_transition_invalid():
    ticket_status = TicketStatusCancelledUser()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    with pytest.raises(InvalidStatus):
        ticket.status_to_confirmed()


def test_ticket_status_to_executed():
    ticket_status = TicketStatusAccepted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    ticket.status_to_executed()
    assert isinstance(ticket.active_status, TicketStatusExecuted)


def test_ticket_status_to_cancelled_operator():
    ticket_status = TicketStatusConfirmed()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status], describe="describe")
    ticket.status_to_cancelled_operator()
    assert isinstance(ticket.active_status, TicketStatusCancelledOperator)
