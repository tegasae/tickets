import sqlite3

from src.adapters.repository import AbstractRepositoryClient
from src.domain.status import ClientStatusOperation
from src.domain.ticket import Client




class SQLiteRepositoryClient(AbstractRepositoryClient):

    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn

    def _save(self, client: Client) -> Client:
        cursor = self.conn.cursor()

        try:
            if not client.client_id:
                cursor.execute("INSERT INTO clients (name,is_active) VALUES (:name,:is_active)",
                               {'name': client.name, 'is_active': client.status.id})
                client.client_id = cursor.lastrowid
            else:
                cursor.execute("UPDATE clients SET name=:name, is_active=:is_active "
                               "WHERE client_id=:client_id",
                               {'name': client.name, 'is_active': client.status.id,
                                'client_id': client.client_id})
                if cursor.rowcount == 0:
                    client.client_id = 0
        except sqlite3.Error:
            client.client_id = 0

        return client

    def _get(self, client_id: int) -> Client:
        cursor = self.conn.cursor()
        cursor.execute("SELECT c.client_id, c.name, c.is_active FROM clients c "
                       "WHERE c.client_id=:client_id",
                       {'client_id': client_id})
        r = cursor.fetchone()
        if r is None:
            return Client(client_id=0, name="", status=ClientStatusOperation.by_id(0))
        client = Client(client_id=r[0], name=r[1], status=ClientStatusOperation.by_id(r[2]))

        return client

    def _delete(self, client_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM clients WHERE client_id=:client_id", {'client_id': client_id})
        if cursor.rowcount > 0:
            return True
        else:
            return False

    def get_by_name(self, name: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT count(client_id) FROM clients WHERE name=:name", {'name': name})
        r = cursor.fetchone()
        if r[0] > 0:
            return True
        else:
            return False

