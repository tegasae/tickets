import sqlite3

from src.adapters.repository import AbstractRepositoryClient
from src.domain.status import ClientStatusDisabled, ClientStatusEnabled
from src.domain.ticket import Client

ClientStatusId = {
    ClientStatusDisabled: 0,
    ClientStatusEnabled: 1
}


def get_client_status_by_id(status_id: int):
    for i in ClientStatusId.keys():
        if ClientStatusId[i] == status_id:
            return i
    return ClientStatusDisabled


class SQLiteRepositoryClient(AbstractRepositoryClient):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn

    def _save(self, client: Client) -> Client:
        cursor = self.conn.cursor()
        try:
            if not client.client_id:
                cursor.execute("INSERT INTO clients (name,is_active) VALUES (:name,:is_active)",
                               {'client_id': client.client_id, 'name': client.name, 'is_active': client.is_active()})
                client.user_id = cursor.lastrowid
            else:
                cursor.execute("UPDATE clients SET name=:name, is_active=:is_active "
                               "WHERE client_id=:client_id",
                               {'name': client.name, 'is_active': client.is_active(),
                                'client_id': client.client_id})
                if cursor.rowcount == 0:
                    client.user_id = 0
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
            return Client(client_id=0, name="", status=ClientStatusDisabled())
        client_status = get_client_status_by_id(r[2])
        client = Client(client_id=r[0], name=r[1], status=client_status())

        return client

    def _delete(self, client_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM clients WHERE client_id=:client_id", {'client_id': client_id})
        if cursor.rowcount > 0:
            return True
        else:
            return False
