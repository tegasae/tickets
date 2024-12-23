from src.domain.exceptions import UserNotFound, TicketNotFound, InvalidTicket
from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.ticket import Ticket
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ListTicketView, TicketView


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


def cancel_ticket(data_cancel_ticket: DataCancelTicket, uow: AbstractUnitOfWork) -> bool:
    with uow:
        user = uow.users.get(user_id=data_cancel_ticket.user_id)
        if user.user_id == 0:
            raise UserNotFound()

        tickets = uow.tickets.get(user_id=user.user_id)
#############################################
        user.add_tickets(tickets=tickets)
        ticket = user.cancel_ticket(ticket_id=data_cancel_ticket.ticket_id, comment=data_cancel_ticket.comment)
        if ticket.ticket_id == 0:
            raise TicketNotFound()
        uow.tickets.save(user_id=user.user_id, ticket=ticket)

##############################################
        uow.commit()
        return True

def get_all_tickets(user_id:int, uow:AbstractUnitOfWork)->ListTicketView:
        return uow.view_tickets.get_all_tickets(user_id=user_id)


def get_ticket(user_id: int, ticket_id:int,uow: AbstractUnitOfWork) -> TicketView:
    tv=uow.view_tickets.get_ticket(user_id=user_id,ticket_id=ticket_id)
    #if tv.ticket_id==0:
    #    raise TicketNotFound()
    return tv
