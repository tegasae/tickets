from src.domain.status import ClientStatus, ClientStatusEnabled, ClientStatusDisabled


class Client:
    """Класс клиент"""

    def __init__(self, client_id: int, name: str, status: ClientStatus):
        self.client_id = client_id
        self.name = name
        self.status = status

    def enable(self):
        self.status = ClientStatusEnabled()

    def disable(self):
        self.status = ClientStatusDisabled()

    def is_active(self):
        if type(self.status) is ClientStatusEnabled:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.name == other.name:
            return True

    @classmethod
    def empty_client(cls):
        return cls(client_id=0, name="", status=ClientStatusDisabled())


class ClientEmpty(Client):
    def __init__(self, client_id: int = 0, name: str = "", status: ClientStatus = ClientStatusDisabled()):
        super().__init__(0, "", ClientStatusDisabled())


class ClientAlreadyExists(Client):
    @classmethod
    def already_exists(cls, client: Client):
        return cls(client_id=client.client_id, name=client.name, status=client.status)


class ClientWrong(Client):
    def __init__(self, client_id: int = 0, name: str = "", status: ClientStatus = ClientStatusDisabled()):
        super().__init__(client_id=client_id, name=name, status=status)


class ClientsCollect:
    def __init__(self, clients: list[Client] = None):
        if clients is None:
            clients = []
        self.clients = clients
        self.by_name = {}

        for c in clients:
            self.by_name[c.name] = c

    def put_client(self, client: Client) -> bool:
        if type(client) is not Client:
            return False
        self.clients.append(client)
        self.by_name[client.name] = client

        return True

    def delete_client(self, client_id: int):
        for i in self.clients:
            if i.client_id == client_id:
                name = i.name
                self.clients.remove(i)
                try:
                    del (self.by_name, name)
                except KeyError:
                    name = ""

    def create_client(self, client_id: int = 0, name: str = "",
                      status: ClientStatus = ClientStatusDisabled()) -> Client:
        name_prepare = name.lstrip()
        name_prepare = name_prepare.rstrip()
        if not name_prepare:
            return ClientWrong(name=name)
        c = self.by_name.get(name_prepare, None)
        if c is not None:
            return ClientAlreadyExists.already_exists(client=c)
        c = Client(client_id=client_id, name=name_prepare, status=status)
        self.put_client(client=c)
        return c
