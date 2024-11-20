from src.domain.exceptions import UserNotFound
from src.domain.ticket import Ticket
from src.services.uow.unit_of_work import AbstractUnitOfWork

def _check_id(i:int)->bool:



def create_ticket(user_id:int,describe:str,uow: AbstractUnitOfWork)->Ticket:
    if not user_id and type(user_id) is not int:
        raise Exception()
    with uow:
        user=uow.users.get(user_id=user_id)
        if not user.user_id:
            raise UserNotFound()
        ticket = Ticket(describe=describe)
        user.create_ticket(ticket=ticket)
        uow.commit()
        return ticket


def cancel_ticket(user_id:int,ticket_id:int,uqw:AbstractUnitOfWork):
    if not user_id and type(user_id) is not int
