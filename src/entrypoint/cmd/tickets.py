from src.api.cmd.cmd import command_wrapper
from src.api.cmd.descriptor import Command, CommandInt
from src.services.service_layer.ticket import get_ticket, get_all_tickets


@command_wrapper(name="list", descriptor=CommandInt)
def list_tickets(argument: CommandInt) -> str:
    print('list')
    if argument.arg:
        t=get_ticket(user_id=argument.addition['user'].user_id, ticket_id=argument.arg, uow=argument.addition['uow'])
        if t.ticket_id==0:
            return "not found"
        return str(t)
    else:
        tickets=get_all_tickets(user_id=argument.addition['user'].user_id,uow=argument.addition['uow'])
        if len(tickets.list_tickets)==0:
            return "not found"
        return str(tickets)