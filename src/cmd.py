
import sqlite3
from dataclasses import dataclass

from src.domain.input_data import DataForTicket
from src.domain.status import ClientStatusEnabled, UserStatusEnabled
from src.domain.ticket import User, Client
from src.services.service_layer import create_ticket, get_all_tickets
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

@dataclass
class Cmd:
    command:str
    arg:str=""

def parse_cmd(cmd_str:str)->Cmd:
    index = cmd_str.find(" ")

    if index != -1:  # Check if a space exists
        cmd = Cmd(command=cmd_str[:index], arg=cmd_str[index + 1:])
    else:
        cmd = Cmd(command=cmd_str)
    return cmd


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
            if cmd.arg=="":
                ticket_id=0
            else:
                try:
                    ticket_id=int(cmd.arg)
                except ValueError:
                    print("Error value")
                    continue

            if ticket_id:
                print(f"Ticket {ticket_id}")
            else:
                print(get_all_tickets(user_id=user.user_id,uow=uow))



    conn.close()
