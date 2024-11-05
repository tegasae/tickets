from src.domain.status import (
    UserStatus, UserStatusEnabled, UserStatusDisabled,
    TicketStatus, TicketStatusAccepted, TicketStatusConfirmed,
    TicketStatusExecuted, TicketStatusCancelledUser, TicketStatusCancelledOperator,
    ClientStatus, ClientStatusEnabled, ClientStatusDisabled
)
from datetime import datetime


def test_user_status():
    status = UserStatus()
    assert status.name == "User status"
    assert isinstance(status.date, datetime)


def test_user_status_enabled():
    status = UserStatusEnabled()
    assert status.name == "Enable"
    assert isinstance(status.date, datetime)


def test_user_status_disabled():
    status = UserStatusDisabled()
    assert status.name == "Disable"
    assert isinstance(status.date, datetime)


def test_ticket_status():
    status = TicketStatus()
    assert status.name == "Ticket status"
    assert isinstance(status.date, datetime)


def test_ticket_status_accepted():
    status = TicketStatusAccepted()
    assert status.name == "Accepted"
    assert isinstance(status.date, datetime)


def test_ticket_status_confirmed():
    status = TicketStatusConfirmed()
    assert status.name == "Confirmed by an operator"
    assert isinstance(status.date, datetime)


def test_ticket_status_executed():
    status = TicketStatusExecuted()
    assert status.name == "Executed"
    assert isinstance(status.date, datetime)


def test_ticket_status_cancelled_user():
    status = TicketStatusCancelledUser()
    assert status.name == "Cancelled by an user"
    assert isinstance(status.date, datetime)


def test_ticket_status_cancelled_operator():
    status = TicketStatusCancelledOperator()
    assert status.name == "Cancelled by an operator"
    assert isinstance(status.date, datetime)


def test_client_status():
    status = ClientStatus()
    assert status.name == "This is the client status"
    assert isinstance(status.date, datetime)


def test_client_status_enabled():
    status = ClientStatusEnabled()
    assert status.name == "The client is enabled"
    assert isinstance(status.date, datetime)


def test_client_status_disabled():
    status = ClientStatusDisabled()
    assert status.name == "The client is disabled"
    assert isinstance(status.date, datetime)
