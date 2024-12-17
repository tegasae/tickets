
import sqlite3
from dataclasses import dataclass

from src.domain.exceptions import TicketNotFound
from src.domain.input_data import DataForTicket
from src.domain.status import ClientStatusEnabled, UserStatusEnabled
from src.domain.ticket import User, Client
from src.services.service_layer import create_ticket, get_all_tickets, get_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

@dataclass
class Cmd:
    command:str
    arg:str=""

def parse_cmd(cmd_str:str)->Cmd:
    index = cmd_str.find(" ")

    if index != -1:  # Check if a space exists
        c = Cmd(command=cmd_str[:index], arg=cmd_str[index + 1:])
    else:
        c = Cmd(command=cmd_str)
    return c


if __name__ == "__main__":
    client = Client(client_id=1, name='Клиент', status=ClientStatusEnabled())
    user = User(user_id=2, client=client, name="user", status=UserStatusEnabled())
    conn = sqlite3.connect('../data/tickets.db')
    uow = SQLLiteUnitOfWork(connection=conn)

    command=""
    while command.lower() != "exit":
        command = input(">").rstrip()
        cmd=parse_cmd(cmd_str=command)

        if cmd.command == 'create':
            dft = DataForTicket(user_id=user.user_id, describe="123", comment='')
            ticket = create_ticket(data_for_ticket=dft, uow=uow)
        if cmd.command == 'list':
            try:
                if cmd.arg=="":
                    ticket_id=0
                else:
                    ticket_id = int(cmd.arg)

                if ticket_id:
                    print(get_ticket(user_id=user.user_id, ticket_id=ticket_id, uow=uow))
                else:
                    print(get_all_tickets(user_id=user.user_id, uow=uow))
            except ValueError:
                print("Error value")
            except TicketNotFound:
                print("Ticket not found")
            finally:
                continue

    conn.close()
