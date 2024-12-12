import json
import sqlite3

from src.domain.exceptions import TicketNotFound
from src.domain.input_data import DataForTicket
from src.domain.status import ClientStatusEnabled, UserStatusEnabled
from src.domain.ticket import User, Client, Ticket
from src.services.service_layer import create_ticket, get_all_tickets
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork
from src.viewers.tickets import ticket_to_dict, ticket_to_json, list_tickets_to_json

def search_by_id(tickets:list[Ticket],ticket_id:int)->Ticket:
    for t in tickets:
        if ticket_id==t.ticket_id:
            return t
    raise TicketNotFound()


if __name__ == "__main__":
    client = Client(client_id=1, name='Клиент', status=ClientStatusEnabled())
    user = User(user_id=2, client=client, name="user", status=UserStatusEnabled())
    conn = sqlite3.connect('../data/tickets.db')
    uow = SQLLiteUnitOfWork(connection=conn)
    command = ""
    while command != "exit":
        full_command = input(">")
        list_command=full_command.split(' ')
        command=list_command[0].lower()

        #commant='list'
        if command == 'create':
            dft = DataForTicket(user_id=user.user_id, describe="123", comment='')
            ticket = create_ticket(data_for_ticket=dft, uow=uow)
        if command == 'list':
            tickets = get_all_tickets(user_id=user.user_id, uow=uow)
            if len(list_command)>1:
                ticket=search_by_id(tickets=tickets,ticket_id=int(list_command[1]))
                print(ticket_to_json(ticket=ticket))
            else:
                print(list_tickets_to_json(tickets))



    conn.close()
