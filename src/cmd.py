import json
import sqlite3
from dataclasses import dataclass

from src.domain.exceptions import TicketNotFound, InvalidTicket
from src.domain.input_data import DataForTicket, DataCancelTicket
from src.domain.status import ClientStatusEnabled, UserStatusEnabled, UserStatusDisabled
from src.domain.ticket import User, Client
from src.services.service_layer import create_ticket, get_all_tickets, get_ticket, cancel_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

@dataclass
class Cmd:
    command:str
    arg:str=""

def parse_cmd(cmd_str:str)->Cmd:
    index = cmd_str.rstrip().find(" ")
    if index != -1:  # Check if a space exists
        c = Cmd(command=cmd_str[:index].lower(), arg=cmd_str[index + 1:])
    else:
        c = Cmd(command=cmd_str.lower())
    return c


if __name__ == "__main__":
    client = Client(client_id=1, name='Клиент', status=ClientStatusEnabled())
    user = User(user_id=2, client=client, name="user", status=UserStatusDisabled())
    conn = sqlite3.connect('../data/tickets.db')
    uow = SQLLiteUnitOfWork(connection=conn)

    cmd=Cmd(command="",arg="")
    while cmd.command!= "exit":

        cmd=parse_cmd(cmd_str=input(">"))
        if cmd.command=="cancel":
            try:
                d = json.loads(cmd.arg)
                dct=DataCancelTicket(user_id=d['user_id'],ticket_id=d['id'],comment=d['comment'])
                cancel_ticket(dct,uow=uow)
                print(dct.ticket_id)
            except ValueError:
                print("Error value")
            except TicketNotFound:
                print("Ticket not found")

            #finally:
            #    continue

        if cmd.command == 'create':
            try:
                d=json.loads(cmd.arg)
                print(d)
                dft = DataForTicket(user_id=user.user_id, describe=d.get('describe',''), comment=d.get('comment',''))
                ticket = create_ticket(data_for_ticket=dft, uow=uow)
            except (json.decoder.JSONDecodeError, KeyError):
                print("The arguments are wrong")
            except InvalidTicket:
                print("The ticket is wrong")
            finally:
                continue
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
