import pytest
from datetime import datetime
from typing import List
from src.domain.ticket import TicketStatus, TicketStatusAccepted, TicketStatusConfirmed, TicketStatusExecuted, \
    TicketStatusCancelledUser, TicketStatusCancelledOperator, Ticket


class TestTicketStatusClasses:
    """Tests for the TicketStatus hierarchy"""

    def test_base_status(self):
        status = TicketStatus()
        assert status.id == 0
        assert status.name == "Ticket status"
        assert isinstance(status.date, datetime)
        assert status.comment == ""

    def test_accepted_status(self):
        status = TicketStatusAccepted()
        assert status.id == 1
        assert status.name == "Accepted"
        assert isinstance(status.date, datetime)

    def test_confirmed_status(self):
        status = TicketStatusConfirmed()
        assert status.id == 2
        assert status.name == "Confirmed by an operator"

    def test_executed_status(self):
        status = TicketStatusExecuted()
        assert status.id == 3
        assert status.name == "Executed"

    def test_cancelled_user_status(self):
        comment = "User changed mind"
        status = TicketStatusCancelledUser(comment=comment)
        assert status.id == 4
        assert status.name == "Cancelled by an user"
        assert status.comment == comment

    def test_cancelled_operator_status(self):
        comment = "Invalid request"
        status = TicketStatusCancelledOperator(comment=comment)
        assert status.id == 5
        assert status.name == "Cancelled by an operator"
        assert status.comment == comment


class TestTicketCreation:
    """Tests for Ticket initialization"""

    def test_create_with_default_status(self):
        ticket = Ticket(ticket_id=1, describe="Test ticket")
        assert len(ticket.statuses) == 1
        assert isinstance(ticket.statuses[0], TicketStatusAccepted)
        assert ticket.describe == "Test ticket"
        assert ticket.ticket_id == 1

    def test_create_with_custom_statuses(self):
        statuses = [TicketStatusAccepted(), TicketStatusConfirmed()]
        ticket = Ticket(ticket_id=2, describe="Custom status", statuses=statuses)
        assert ticket.statuses == statuses
        assert len(ticket.statuses) == 2

    def test_empty_ticket(self):
        ticket = Ticket.empty_ticket()
        assert ticket.ticket_id == 0
        assert ticket.describe == ""
        assert ticket.statuses == []

    def test_describe_validation(self):
        with pytest.raises(ValueError):
            Ticket(ticket_id=1, describe="")

        with pytest.raises(ValueError):
            Ticket(ticket_id=1, describe="   ")

        ticket = Ticket(ticket_id=1, describe="  Test  ")
        assert ticket.describe == "Test"
