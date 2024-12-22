
import sqlite3

from src.api.cmd.cmd import command_wrapper, cmd_process
from src.api.cmd.descriptor import CommandInt, Command, CommandJSON
from src.domain.exceptions import TicketNotFound, InvalidTicket
from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.status import ClientStatusEnabled, UserStatusEnabled, UserStatusDisabled
from src.domain.ticket import User, Client
from src.services.service_layer import create_ticket, get_all_tickets, get_ticket, cancel_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork





@command_wrapper(name="list",descriptor=Command)
def get_all(argument:Command):
    print(get_all_tickets(user_id=argument.user.user_id, uow=argument.uow))

@command_wrapper(name="get",descriptor=CommandInt)
def get_all(argument:CommandInt):
    print(get_ticket(user_id=argument.user.user_id, ticket_id=argument.arg, uow=uow))


@command_wrapper(name="cancel",descriptor=CommandJSON)
def cancel(argument:CommandJSON):
    dct = DataCancelTicket(user_id=argument.arg['user_id'], ticket_id=argument.arg['id'], comment=argument.arg['comment'])
    cancel_ticket(dct, uow=argument.uow)
    print(dct.ticket_id)


@command_wrapper(name="exit",descriptor=Command)
def exit_program(argument:Command):
    exit()


@command_wrapper(name="create",descriptor=CommandJSON)
def create(argument:CommandJSON):
    dft = DataForTicket(user_id=argument.user.user_id, describe=argument.arg.get('describe', ''), comment=argument.arg.get('comment', ''))
    ticket1 = create_ticket(data_for_ticket=dft, uow=argument.uow)
    print(ticket1.ticket_id)

if __name__ == "__main__":
    client = Client(client_id=1, name='Клиент', status=ClientStatusEnabled())
    user = User(user_id=2, client=client, name="user", status=UserStatusDisabled())
    conn = sqlite3.connect('../data/tickets.db')
    uow = SQLLiteUnitOfWork(connection=conn)

    cmd_process(uow=uow,user=user)
    conn.close()
