from dataclasses import dataclass
from typing import Type

from src.domain.messages import Message, EventClientWronged, EventClientCreated, EventClientCantDeleted, \
    EventClientDeleted, EventClientUpdated, EventClientDisabled


@dataclass(frozen=True)
class ClientStatus:
    id:int = 0
    status:str="undefined"

@dataclass(frozen=True)
class ClientStatusEnabled(ClientStatus):
    id:int = 1
    status:str = "enabled"

@dataclass(frozen=True)
class ClientStatusDisabled(ClientStatus):
    id:int = 2
    status:str = "disabled"


_list_of_status = (ClientStatus, ClientStatusEnabled, ClientStatusDisabled)


class ClientStatusOperation:
    @staticmethod
    def by_id(status_id: int) -> ClientStatus:
        """Retrieve a ClientStatus instance by its ID."""
        for status in _list_of_status:
            if status.id == status_id:
                return status()
        return _list_of_status[0]()  # Default to the first status

    @staticmethod
    def by_type(client_status_type: Type[ClientStatus]) -> int:
        """Retrieve the ID of a given ClientStatus type."""
        for status in _list_of_status:
            if client_status_type is status:
                return status.id
        return _list_of_status[0].id  # Default to the first status ID

    @staticmethod
    def by_enable(enable: bool) -> ClientStatus:
        """Retrieve ClientStatus based on the enable flag."""
        return ClientStatusEnabled() if enable else ClientStatusDisabled()


@dataclass(kw_only=True)
class Client:
    client_id:int
    name:str
    code:str
    status:ClientStatus=ClientStatusEnabled()


@dataclass(kw_only=True)
class ClientEmpty(Client):
    client_id:int = 0
    name: str = ""
    code: str = ""
    status: ClientStatus = ClientStatusDisabled()


@dataclass(kw_only=True)
class ClientWrong(Client):
    client_id:int = 0
    name: str = ""
    code: str = ""
    status: ClientStatus = ClientStatusDisabled()


class ClientCollection:
    """Manages a collection of clients."""

    def __init__(self, clients: list[Client] = None):
        self.by_id: dict[int, Client] = {}

        if type(clients) is list:
            for c in clients:
                if type(c) is Client:
                    self.by_id[c.client_id] = c
        self.events: list[Message] = []

    def create_client(self,client_id:int, name:str,code:str,status:ClientStatus)->Client:
        prepared_named = name.strip()
        if len(prepared_named)==0:
            self.events.append(EventClientWronged(name=name))
            return ClientWrong(name=name)
        return Client(client_id=client_id,name=name,code=code,status=status)

    def get_clients(self)->list[Client]:
        return list(self.by_id.values())

    def put_client(self, client: Client) -> Client:
        """Add or update a client in the collection."""
        if client.client_id in self.by_id:
            self.events.append(EventClientUpdated(client_id=client.client_id))
        else:
            self.events.append(EventClientCreated(client_id=client.client_id))
        self.by_id[client.client_id]=client
        return client


    def disable(self,client_id:int)->Client:
        client=self.by_id.get(client_id,ClientEmpty())

        if type(client) is not ClientEmpty:
            client.status=ClientStatusDisabled()
            self.events.append(EventClientDisabled(client_id=client_id))
        return client

    def enable(self,client_id:int)->Client:
        client = self.by_id.get(client_id, ClientEmpty())
        if type(client) is not ClientEmpty:
            client.status = ClientStatusEnabled()
        return client

    def delete_id(self, client_id: int) -> bool:
        """Delete a client by their ID."""
        try:
            del(self.by_id[client_id])
            self.events.append(EventClientDeleted())
            return True
        except KeyError:
            self.events.append(EventClientCantDeleted())
            return False

