
from typing import Type

from src.domain.messages import Message, EventClientWronged, EventClientAlreadyExists, EventClientCreated, \
    EventClientUpdated, EventClientCantDeleted, EventClientDeleted


class ClientStatus:
    id = 0


class ClientStatusEnabled(ClientStatus):
    id = 1


class ClientStatusDisabled(ClientStatus):
    id = 2


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


class ClientCollection:
    """Manages a collection of clients."""

    def __init__(self, clients: list[Client] = None):
        self.clients = []
        if clients is not None:
            self.clients = clients

        self.by_name: dict[str, Client] = {}
        self.by_id: dict[int, Client] = {}

        c: Client
        for c in self.clients:
            if type(c) is Client:
                self.by_name[c.name] = c
                if c.client_id != 0:
                    self.by_id[c.client_id] = c
        self.events: list[Message] = []

    @staticmethod
    def create_client(client_id: int = 0, name: str = "",
                      status: ClientStatus = ClientStatusDisabled()) -> Client:
        """Create a new client instance."""

        prepared_name = name.strip()

        if len(prepared_name) == 0:
            return ClientWrong(name=name)
        return Client(client_id=client_id, name=prepared_name, status=status)

    def get_client(self):
        for c in self.by_name:
            yield c

    def put_client(self, client: Client) -> Client:
        """Add or update a client in the collection."""
        if type(client) is not Client:
            self.events.append(EventClientWronged(name=client.name))
            return client
        prepared_named = client.name.strip()
        if len(prepared_named) == 0:
            self.events.append(EventClientWronged(name=client.name))
            return ClientWrong(name=client.name)

        client.name = prepared_named

        # existing_client = self.by_name.get(client.name, ClientEmpty())

        if client.client_id == 0:
            existing_client = self.by_name.get(client.name, ClientEmpty())
            if client.name == existing_client.name and existing_client.client_id != 0:
                self.events.append(EventClientAlreadyExists(client_id=client.client_id))
                return ClientAlreadyExists.already_exists(client)
            self.by_name[client.name] = client
            self.events.append(EventClientCreated(client_id=client.client_id))
            return client

        if client.client_id != 0:
            existing_client = self.by_name.get(client.name, ClientEmpty())
            existing_client_id = self.by_id.get(client.client_id, ClientEmpty())
            if type(existing_client) is ClientEmpty and type(existing_client_id) is ClientEmpty:
                self.by_name[client.name] = client
                self.by_id[client.client_id] = client
                self.events.append(EventClientUpdated(client_id=client.client_id))
                return client

            if existing_client.name == client.name and existing_client.client_id == 0:
                self.by_name[client.name] = client
                self.by_id[client.client_id] = client
                self.events.append(EventClientUpdated(client_id=client.client_id))
                return client

            if existing_client.name == client.name and existing_client.client_id == client.client_id and \
                    existing_client_id.name == client.name and existing_client_id.client_id == client.client_id:
                self.by_name[client.name] = client
                self.by_id[client.client_id] = client
                self.events.append(EventClientUpdated(client_id=client.client_id))
                return client
            if existing_client.name == client.name and existing_client.client_id != client.client_id:
                self.events.append(EventClientAlreadyExists(client_id=client.client_id))
                return ClientAlreadyExists.already_exists(client)

            if existing_client.name != client.name and existing_client_id.client_id == client.client_id:
                try:
                    del (self.by_name[existing_client_id.name])
                finally:
                    self.by_name[client.name] = client
                    self.by_id[client.client_id] = client
                self.events.append(EventClientUpdated(client_id=client.client_id))
                return client
        self.events.append(EventClientWronged(name=client.name))
        return ClientWrong()

    def delete_name(self, name: str) -> bool:
        try:
            client = self.by_name.get(name, ClientEmpty)
            del (self.by_name[name])
            self.events.append(EventClientDeleted())
        except KeyError:
            self.events.append(EventClientCantDeleted())
            return False

        try:
            del(self.by_id[client.client_id])
        finally:
            self.events.append(EventClientDeleted())
            return True

    def delete_id(self, client_id: int) -> bool:
        """Delete a client by their ID."""
        try:
            client = self.by_id.get(client_id, ClientEmpty)
            del(self.by_id[client_id])
            del(self.by_name[client.name])
            self.events.append(EventClientDeleted())
            return True
        except KeyError:
            self.events.append(EventClientCantDeleted())
            return False
