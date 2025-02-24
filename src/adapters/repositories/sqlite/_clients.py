from src.adapters.repository import AbstractRepositoryClientCollection
from src.domain.client import Client,  ClientStatusOperation, ClientCollection
from src.domain.exceptions import ErrorWithStore
from src.utils.dbapi.connect import Connection
from src.utils.dbapi.exceptions import DBOperationError


class SQLiteRepositoryClientCollection(AbstractRepositoryClientCollection):

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.insert = self.conn.create_query("INSERT INTO clients (name,is_active,code1s) VALUES (:name,:is_active,:code)")
        self.update = self.conn.create_query(
                                "UPDATE clients SET name=:name, is_active=:is_active,code1s=:code WHERE client_id=:client_id")
        self.get_all = self.conn.create_query("SELECT c.client_id, c.name, c.is_active, c.code1s FROM clients c")
        self.remove = self.conn.create_query("DELETE FROM clients WHERE client_id=:client_id")

    def _add(self,client:Client)->Client:
        try:
            if not client.client_id:
                client.client_id = self.insert.set_result(params={'name': client.name, 'is_active': client.status.id, 'code': client.code})
            else:
                self.update.set_result(params={'name': client.name, 'is_active': client.status.id, 'code': client.code,
                                           'client_id': client.client_id})
                if self.update.count==0:
                    raise ErrorWithStore("The client didn't find")
            return client
        except DBOperationError as e:
            raise ErrorWithStore(e)


    def _save(self, client_collection: ClientCollection) -> ClientCollection:
        for c in client_collection.get_clients():
               c=self._add(client=c)
        return client_collection

    def _get(self) -> ClientCollection:
        try:

            r = self.get_all.get_result()
            clients=[]
            for c in r:
                client=Client(client_id=c[0], name=c[1],status=ClientStatusOperation.by_id(c[2]),code=c[3])
                clients.append(client)
            client_collection = ClientCollection(clients=clients)
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

