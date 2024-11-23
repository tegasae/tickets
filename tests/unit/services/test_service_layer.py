import pytest

from src.domain.exceptions import UserNotFound
from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.status import UserStatusEnabled
from src.domain.ticket import Ticket, User
from src.services.service_layer import create_ticket, cancel_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork
from tests.conftest import get_client


def test_create_ticket(create_conn, get_user):
    uow = SQLLiteUnitOfWork(connection=create_conn)

    dft = DataForTicket(user_id=get_user.user_id, describe="123")
    ticket = create_ticket(data_for_ticket=dft, uow=uow)
    assert ticket.ticket_id == 1
    dft = DataForTicket(user_id=10, describe="123")
    with pytest.raises(UserNotFound):
        ticket = create_ticket(data_for_ticket=dft, uow=uow)


def test_cancel_ticket(create_conn, get_user):
    uow = SQLLiteUnitOfWork(connection=create_conn)
    ticket = Ticket(describe="123")
    user = User(user_id=0, client=get_client(), name="user", status=UserStatusEnabled())
    uow.users.save(user=user)
    uow.tickets.save(user_id=user.user_id, ticket=ticket)
    user.create_ticket(ticket)
    dct = DataCancelTicket(user_id=user.user_id, ticket_id=1)
    r = cancel_ticket(data_cancel_ticket=dct, uow=uow)
    assert r == True
