from src.adapters.repository import AbstractRepositoryClientCollection
from src.domain.client import Client, ClientEmpty, ClientStatusOperation, ClientCollection
from src.domain.exceptions import ErrorWithStore
from src.utils.dbapi.connect import Connection
from src.utils.dbapi.exceptions import DBOperationError


class SQLiteRepositoryClientCollection(AbstractRepositoryClientCollection):

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.insert = self.conn.create_query("INSERT INTO clients (name,is_active) VALUES (:name,:is_active)")
        self.update = self.conn.create_query(
                                "UPDATE clients SET name=:name, is_active=:is_active WHERE client_id=:client_id")
        self.get_all = self.conn.create_query("SELECT c.client_id, c.name, c.is_active FROM clients c")
        self.remove = self.conn.create_query("DELETE FROM clients WHERE client_id=:client_id")
        self.find_name = self.conn.create_query("SELECT client_id, name, is_active client_id "
                                                "FROM clients WHERE name=:name")

    def _save(self, client_collection: ClientCollection) -> ClientCollection:
        try:
            for c in client_collection.get_clients():
                if not c.client_id:
                    c.client_id = self.insert.set_result(params={'name': c.name, 'is_active': c.status.id})
                else:
                    self.update.set_result(params={'name': c.name, 'is_active': c.status.id,
                                                         'client_id': c.client_id})

                client_collection.put_client(client=c)
            return client_collection
        except DBOperationError as e:
            raise ErrorWithStore(e)

    def _get(self) -> ClientCollection:
        try:
            client_collection=ClientCollection()
            r = self.get_all.get_result()
            for c in r:
                client_collection.put_client(Client(client_id=c[0], name=c[1], status=ClientStatusOperation.by_id(c[2])))
            return client_collection
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

