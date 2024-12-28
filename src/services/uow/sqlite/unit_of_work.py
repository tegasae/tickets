import sqlite3

from src.adapters.repositories.sqlite import SQLiteRepositoryUser, SQLiteRepositoryTicket, SQLiteRepositoryClient
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.sqlite.clients import SQLiteClientViewer
from src.viewers.sqlite.tickets import SQLiteTicketViewer


class SQLLiteUnitOfWork(AbstractUnitOfWork):
    def __init__(self, connection:sqlite3.Connection):
        self.connection=connection
        self.users=SQLiteRepositoryUser(conn=self.connection)
        self.tickets = SQLiteRepositoryTicket(conn=self.connection)
        self.clients=SQLiteRepositoryClient(conn=self.connection)
        self.view_tickets=SQLiteTicketViewer(conn=self.connection)
        self.view_clients = SQLiteClientViewer(conn=self.connection)

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        #self.connection.close()

    def _commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()