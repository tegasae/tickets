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

    @classmethod
    def empty_client(cls):
        return cls(client_id=0, name="", status=ClientStatusDisabled())


