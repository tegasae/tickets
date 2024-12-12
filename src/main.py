import sqlite3

from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.status import TicketStatusConfirmed, TicketStatusAccepted
from src.services.service_layer import create_ticket, cancel_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

if __name__=='__main__':
    conn=sqlite3.connect('../data/tickets.db')
    uow=SQLLiteUnitOfWork(connection=conn)
    user=uow.users.get(user_id=2)

    dft=DataForTicket(user_id=user.user_id, describe="123",comment='')
    ticket=create_ticket(data_for_ticket=dft, uow=uow)
    print(ticket)
    ticket.statuses.append(TicketStatusConfirmed())
    with uow:
        uow.tickets.save(user_id=2,ticket=ticket)
        uow.commit()
    dct=DataCancelTicket(user_id=2,ticket_id=ticket.ticket_id,comment='123')
    cancel_ticket(uow=uow,data_cancel_ticket=dct)

    conn.close()