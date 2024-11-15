
from src.domain.exceptions import CommonException, InvalidStatus, InvalidTicket


def test_common_exception():
    ex = CommonException("Test message")
    assert ex.base_message == "Test message"
    assert str(ex) == "Test message"


def test_invalid_status():
    ex = InvalidStatus("Invalid status provided")
    assert ex.base_message == "The status isn't correct Invalid status provided"
    assert str(ex) == "The status isn't correct Invalid status provided"


def test_invalid_ticket():
    ex = InvalidTicket("Ticket ID not found")
    assert ex.base_message == "The ticket isn't correct Ticket ID not found"
    assert str(ex) == "The ticket isn't correct Ticket ID not found"
