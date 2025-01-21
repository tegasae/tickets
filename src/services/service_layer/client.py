from src.domain.input_data import DataClient
from src.domain.messages import AlreadyExitedClient, ClientEvents, CantStoredClient, CreatedClient, DeletedClient, \
    NotDeletedClient
from src.domain.status import ClientStatusOperation
from src.domain.client import Client, ClientWrong
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(dc: DataClient, uow: AbstractUnitOfWork) -> ClientEvents:
    with uow:
        status = ClientStatusOperation.by_enable(dc.enable)
        client = Client(client_id=dc.client_id, name=dc.name, status=status)
        if uow.clients.find_by_name(dc.name):
            return AlreadyExitedClient(client=client, name=dc.name)
        status = ClientStatusOperation.by_enable(dc.enable)
        client = Client(client_id=dc.client_id, name=dc.name, status=status)
        client = uow.clients.save(client=client)
        if client.client_id == 0:
            return CantStoredClient(client=client)
        uow.commit()
        return CreatedClient(client=client)


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    tc = uow.view_clients.get_client(client_id=client_id)
    return tc


def list_clients(uow: AbstractUnitOfWork) -> list[ClientView]:
    return uow.view_clients.get_all_clients()


def delete_client(client_id: int, uow: AbstractUnitOfWork) -> ClientEvents:
    with uow:
        if not uow.clients.delete(client_id=client_id):
            return NotDeletedClient(client=ClientWrong())
        uow.commit()
    return DeletedClient(client=ClientWrong())
