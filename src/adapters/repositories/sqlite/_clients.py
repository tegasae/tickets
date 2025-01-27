from src.adapters.repository import AbstractRepositoryClient
from src.domain.client import Client, ClientEmpty, ClientStatusOperation
from src.domain.exceptions import ErrorWithStore
from src.utils.dbapi.connect import Connection
from src.utils.dbapi.exceptions import DBOperationError


class SQLiteRepositoryClient(AbstractRepositoryClient):

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.insert = self.conn.create_query("INSERT INTO clients (name,is_active) VALUES (:name,:is_active)")
        self.update = self.conn.create_query(
            "UPDATE clients SET name=:name, is_active=:is_active WHERE client_id=:client_id")
        self.get_id = self.conn.create_query("SELECT c.client_id, c.name, c.is_active "
                                             "FROM clients c WHERE c.client_id=:client_id",
                                             params=['id', 'name', 'is_active'])
        self.remove = self.conn.create_query("DELETE FROM clients WHERE client_id=:client_id")
        self.find_name = self.conn.create_query("SELECT client_id, name, is_active client_id "
                                                "FROM clients WHERE name=:name")

    def _save(self, client: Client) -> Client:
        try:
            if not client.client_id:
                client.client_id = self.insert.set_result(params={'name': client.name, 'is_active': client.status.id})
            else:
                last_id = self.update.set_result(params={'name': client.name, 'is_active': client.status.id,
                                                         'client_id': client.client_id})
                #if last_id == 0:
                #    client.client_id = 0
            return client
        except DBOperationError as e:
            raise ErrorWithStore(e)


    def _get(self, client_id: int) -> Client:
        try:
            r = self.get_id.get_one_result(var={client_id: client_id})
            if len(r) == 0:
                return ClientEmpty()
            return Client(client_id=r[0], name=r[1], status=ClientStatusOperation.by_id(r[2]))
        except DBOperationError as e:
            raise ErrorWithStore(e)


    def _delete(self, client_id: int) -> bool:
        try:
            self.remove.set_result(params={"client_id": client_id})
            if self.remove.count > 0:
                return True
            else:
                return False
        except DBOperationError as e:
            raise ErrorWithStore(e)

    def find_by_name(self, name: str) -> Client:
        try:
            r = self.find_name.get_one_result(params={"name": name})
            if len(r) == 0:
                return ClientEmpty()
            else:
                return Client(client_id=r[0], name=r[1], status=ClientStatusOperation.by_id(r[2]))
        except DBOperationError as e:
            raise ErrorWithStore(e)
