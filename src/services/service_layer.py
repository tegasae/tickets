from src.domain.exceptions import UserNotFound, TicketNotFound
from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.status import UserStatusEnabled
from src.domain.ticket import Ticket, User
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork
from src.services.uow.unit_of_work import AbstractUnitOfWork
from tests.conftest import create_conn, get_client, create_db_sqlite


def create_ticket(data_for_ticket: DataForTicket, uow: AbstractUnitOfWork) -> Ticket:
    with uow:
        user = uow.users.get(user_id=data_for_ticket.user_id)
        if not user.user_id:
            raise UserNotFound()
        ticket = Ticket(describe=data_for_ticket.describe)
        user.create_ticket(ticket=ticket)
        uow.tickets.save(user_id=user.user_id, ticket=ticket)
        uow.commit()
        return ticket
    return Ticket(ticket_id=0, describe=data_for_ticket.describe)


def cancel_ticket(data_cancel_ticket: DataCancelTicket, uow: AbstractUnitOfWork) -> bool:
    with uow:
        user = uow.users.get(user_id=data_cancel_ticket.user_id)

        if user.user_id == 0:
            raise UserNotFound()
        tickets = uow.tickets.get(user_id=user.user_id)
        #user.tickets = tickets
        for t in tickets:
            user.create_ticket(t)
        ticket = user.cancel_ticket(ticket_id=data_cancel_ticket.ticket_id, comment=data_cancel_ticket.comment)

        if ticket.ticket_id == 0:
            raise TicketNotFound()
        uow.tickets.save(user_id=user.user_id, ticket=ticket)
        uow.commit()
        return True
    return False

if __name__=='__main__':
    uow = SQLLiteUnitOfWork(connection=create_db_sqlite(schema='../../data/schema.sql'))
    ticket = Ticket(describe="123")
    user = User(user_id=0, client=get_client(), name="user", status=UserStatusEnabled())
    uow.users.save(user=user)
    uow.tickets.save(user_id=user.user_id, ticket=ticket)
    user.create_ticket(ticket)
    dct = DataCancelTicket(user_id=user.user_id, ticket_id=1)
    r = cancel_ticket(data_cancel_ticket=dct, uow=uow)