from src.domain.input_data import DataClient
from src.domain.client import Client, ClientWrong, ClientStatusOperation, ClientsCollect, ClientAlreadyExists
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(dc: DataClient, uow: AbstractUnitOfWork) -> Client:
    with uow:
        client_collect=ClientsCollect()
        client=Client(client_id=dc.client_id,name=dc.name,status=ClientStatusOperation.by_enable(dc.enable))
        client_check=uow.clients.find_by_name(client.name)
        client_check = client_collect.put_client(client=client_check)
        client=client_collect.put_client(client=client)
        if type(client) is ClientAlreadyExists:
            return client
        if type(client) is Client:
            client = uow.clients.save(client=client)
        else:
            return client

        uow.commit()
        return client


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    return uow.view_clients.get_client(client_id=client_id)


def list_clients(uow: AbstractUnitOfWork) -> list[ClientView]:
    return uow.view_clients.get_all_clients()


def delete_client(client_id: int, uow: AbstractUnitOfWork) -> bool:
    with uow:
        if not uow.clients.delete(client_id=client_id):
            return False
        uow.client_collect.delete_id(client_id=client_id)
        uow.commit()
    return True
