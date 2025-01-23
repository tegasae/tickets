from src.domain.input_data import DataClient
from src.domain.messages import AlreadyExitedClient, ClientEvents, CantStoredClient, CreatedClient, DeletedClient, \
    NotDeletedClient
from src.domain.status import ClientStatusOperation
from src.domain.client import Client, ClientWrong, ClientsCollect
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(dc: DataClient, uow: AbstractUnitOfWork) -> ClientEvents:
    with uow:
        #Создаем Client
        client=Client(client_id=dc.client_id,name=dc.name,status=ClientStatusOperation.by_enable(dc.enable))

        #uow.client_collect.create_client(client_id=client_already_exists.client_id,name=client_already_exists.name,status=client_already_exists.status)
        #client=uow.client_collect.create_client(client_id=dc.client_id,name=dc.name,status=ClientStatusOperation.by_enable(dc.enable))
        #if type(client) is client:
        #    client = uow.clients.save(client=client)
        #else:
        #    return CantStoredClient(client=client)
        #if client.client_id == 0:
        #    return CantStoredClient(client=client)
        #uow.commit()
        #return CreatedClient(client=client)


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    return uow.view_clients.get_client(client_id=client_id)


def list_clients(uow: AbstractUnitOfWork) -> list[ClientView]:
    return uow.view_clients.get_all_clients()


def delete_client(client_id: int, uow: AbstractUnitOfWork) -> ClientEvents:
    with uow:
        if not uow.clients.delete(client_id=client_id):
            return NotDeletedClient(client=ClientWrong())
        uow.client_collect.delete_client(client_id=client_id)
        uow.commit()
    return DeletedClient(client=ClientWrong())
