from src.domain.input_data import DataClient
from src.domain.client import Client, ClientStatusOperation, ClientsCollect
from src.domain.messages import EventClientDeleted, EventClientCantDeleted
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(dc: DataClient, uow: AbstractUnitOfWork) -> Client:
    with uow:
        client = Client(client_id=dc.client_id, name=dc.name, status=ClientStatusOperation.by_enable(dc.enable))
        client_check = uow.clients.find_by_name(client.name)
        client_collect = ClientsCollect(clients=[client_check])
        client = client_collect.put_client(client=client)
        if type(client) is not Client:
            return client

        client = uow.clients.save(client=client)
        uow.events+=client_collect.events
        client_collect.events.clear()
        uow.commit()
        return client


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    return uow.view_clients.get_client(client_id=client_id)


def list_clients(uow: AbstractUnitOfWork) -> list[ClientView]:
    return uow.view_clients.get_all_clients()


def delete_client(client_id: int, uow: AbstractUnitOfWork) -> bool:
    with uow:

        if not uow.clients.delete(client_id=client_id):
            uow.events.append(EventClientCantDeleted())
            return False
        #client_collect.delete_id(client_id=client_id)
        #uow.events += client_collect.events

        #client_collect.events.clear()
        uow.commit()
    uow.events.append(EventClientDeleted())
    return True
