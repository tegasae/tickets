import pytest

from src.domain.exceptions import InvalidStatus
from src.domain.status import UserStatusEnabled, ClientStatusEnabled, ClientStatusDisabled, UserStatusDisabled, \
    TicketStatusAccepted, TicketStatusCancelledUser, TicketStatusExecuted
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
    assert user.is_active() is False


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
    t=user.cancel_ticket(ticket_id=1, comment="comment")
    t1=user.cancel_ticket(ticket_id=2, comment="comment")

    assert t.ticket_id!=0
    assert t1.ticket_id==0
    assert isinstance(user.tickets[1].active_status, TicketStatusCancelledUser)


def test_user_cannot_cancel_ticket():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[], status=user_status)
    ticket_status = TicketStatusAccepted()
    ticket_status_executed = TicketStatusExecuted()
    ticket = Ticket(ticket_id=1, statuses=[ticket_status,ticket_status_executed], describe="describe")
    user.create_ticket(ticket)

    with pytest.raises(InvalidStatus):
        user.cancel_ticket(ticket_id=1, comment="comment")


def test_user_create_tickets():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    user_status = UserStatusEnabled()
    user = User(user_id=1, name="Test User", client=client, tickets=[Ticket(ticket_id=1,describe="decribe1"),Ticket(ticket_id=2, describe="describe2")], status=user_status)
    assert len(user.tickets)==2