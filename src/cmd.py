import json
import sqlite3

from src.domain.input_data import DataForTicket
from src.domain.status import ClientStatusEnabled, UserStatusEnabled
from src.domain.ticket import User, Client
from src.services.service_layer import create_ticket, get_all_tickets
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

if __name__ == "__main__":
    client = Client(client_id=1, name='Клиент', status=ClientStatusEnabled())
    user = User(user_id=2, client=client, name="user", status=UserStatusEnabled())
    conn = sqlite3.connect('../data/tickets.db')
    uow = SQLLiteUnitOfWork(connection=conn)
    command = ""
    while command.lower() != "exit":
        command = input(">")
        #commant='list'
        if command == 'create':
            dft = DataForTicket(user_id=user.user_id, describe="123", comment='')
            ticket = create_ticket(data_for_ticket=dft, uow=uow)
        if command == 'list':
            tickets = get_all_tickets(user_id=user.user_id, uow=uow)

            print(json.dump(tickets))

    conn.close()
