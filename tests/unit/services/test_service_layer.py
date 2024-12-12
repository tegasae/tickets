import pytest

from src.domain.exceptions import UserNotFound, TicketNotFound
from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.status import UserStatusEnabled
from src.domain.ticket import Ticket, User
from src.services.service_layer import create_ticket, cancel_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork
from tests.conftest import get_client


def test_create_ticket(create_conn, get_user):
    uow = SQLLiteUnitOfWork(connection=create_conn)

    dft = DataForTicket(user_id=get_user.user_id, describe="123",comment="")
    ticket = create_ticket(data_for_ticket=dft, uow=uow)
    assert ticket.ticket_id == 1
    dft = DataForTicket(user_id=10, describe="123",comment="1")
    with pytest.raises(UserNotFound):
        ticket = create_ticket(data_for_ticket=dft, uow=uow)


def test_cancel_ticket(create_conn, get_user):
    uow = SQLLiteUnitOfWork(connection=create_conn)
    ticket = Ticket(describe="123")
    user = User(user_id=0, client=get_client(), name="user", status=UserStatusEnabled())
    uow.users.save(user=user)
    uow.tickets.save(user_id=user.user_id, ticket=ticket)
    user.create_ticket(ticket)
    dct = DataCancelTicket(user_id=user.user_id, ticket_id=1,comment="123")
    r = cancel_ticket(data_cancel_ticket=dct, uow=uow)

    assert r is True
    with pytest.raises(TicketNotFound):
        dct = DataCancelTicket(user_id=user.user_id, ticket_id=2,comment="1111")
        r = cancel_ticket(data_cancel_ticket=dct, uow=uow)

    dct = DataCancelTicket(user_id=user.user_id+1, ticket_id=1,comment="1234")
    with pytest.raises(UserNotFound):
        r = cancel_ticket(data_cancel_ticket=dct, uow=uow)