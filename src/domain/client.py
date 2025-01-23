from typing import Optional, List

from src.domain.status import ClientStatus, ClientStatusEnabled, ClientStatusDisabled


class Client:
    """Represents a client with an ID, name, and status."""

    def __init__(self, client_id: int, name: str, status: ClientStatus):
        self.client_id = client_id
        self.name = name
        self.status = status

    def enable(self):
        """Enable the client."""
        self.status = ClientStatusEnabled()

    def disable(self):
        """Disable the client."""
        self.status = ClientStatusDisabled()

    def is_active(self) -> bool:
        """Check if the client is active."""
        return isinstance(self.status, ClientStatusEnabled)


    @classmethod
    def empty_client(cls) -> "Client":
        """Create an empty client instance."""
        return cls(client_id=0, name="", status=ClientStatusDisabled())


class ClientEmpty(Client):
    """Represents an empty client."""
    def __init__(self):
        super().__init__(client_id=0, name="", status=ClientStatusDisabled())


class ClientAlreadyExists(Client):
    """Represents a client that already exists."""

    @classmethod
    def already_exists(cls, client: "Client") -> "ClientAlreadyExists":
        """Create a new instance representing an already existing client."""
        return cls(client_id=client.client_id, name=client.name, status=client.status)


class ClientWrong(Client):
    """Represents a wrongly configured client."""
    def __init__(self, client_id: int = 0, name: str = "", status: ClientStatus = ClientStatusDisabled()):
        super().__init__(client_id=client_id, name=name, status=status)


class ClientsCollect:
    """Manages a collection of clients."""

    def __init__(self, clients: Optional[List[Client]] = None):
        self.by_name = {client.name: client for client in clients if client.client_id!=0}
        self.by_id={client.client_id: client for client in clients if client.client_id!=0}

    @staticmethod
    def create_client(client_id: int = 0, name: str = "",
                      status: ClientStatus = ClientStatusDisabled()) -> Client:
        """Create a new client instance."""

        prepared_name = name.strip()

        if len(prepared_name)==0:
            return ClientWrong(name=name)
        return Client(client_id=client_id, name=prepared_name, status=status)

    def _add_client(self,client:Client):
        if client.client_id!=0:
            self.by_id[client.client_id]=client
            self.by_name[client.name] = client

    def _get_by_name(self,name:str)->Client:
        client=self.by_name.get(name,None)
        if client is None:
            return ClientEmpty()
        else:
            return client

    def put_client(self, client: Client) -> Client:
        """Add or update a client in the collection."""
        if type(client) is not Client:
            return client

        existing_client = self._get_by_name(client.name)

        if type(existing_client) is not ClientEmpty:
            if client.client_id==0 and client.name==existing_client.name:
                return ClientAlreadyExists.already_exists(existing_client)
            if client.client_id!=0 and client.client_id!=existing_client.client_id and client.name==existing_client.name:
                return ClientAlreadyExists.already_exists(existing_client)
        self._add_client(client)
        return client

    def delete_client(self, client_id: int) -> bool:
        """Delete a client by their ID."""
        client=self.by_id.get(client_id,ClientEmpty)
        try:
            del(self.by_id[client.client_id])
            del(self.by_name[client.name])
            return True
        except KeyError:
            return False
