import sqlite3

from src.api.cmd.cmd import cmd_process, command_wrapper

from src.domain.status import ClientStatusEnabled, UserStatusEnabled, UserStatusDisabled
from src.domain.ticket import User, Client
from src.entrypoint.cmd.tickets import *
from src.entrypoint.cmd.clients import *

from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork



if __name__ == "__main__":
    client = Client(client_id=1, name='Клиент', status=ClientStatusEnabled())
    user = User(user_id=2, client=client, name="user", status=UserStatusDisabled())
    conn = sqlite3.connect('../data/tickets.db')
    uow = SQLLiteUnitOfWork(connection=conn)

    cmd_process(uow=uow, user=user)
    conn.close()
