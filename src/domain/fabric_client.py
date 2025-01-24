from src.domain.client import Client, ClientStatus, ClientStatusDisabled
from src.domain.messages import ClientEvents, CantCreatedClient, CreatedClient


def create_client(client_id: int = 0, name: str = "", status: ClientStatus = ClientStatusDisabled()) -> ClientEvents:

    name_prepare = name.lstrip()
    name = name_prepare.rstrip()
    if not name_prepare:
        return CantCreatedClient(client=Client.empty_client(), name=name)
    return CreatedClient(client=Client(client_id=client_id, name=name, status=status))
