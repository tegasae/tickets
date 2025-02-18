from src.domain.input_data import DataClient
from src.domain.client import Client, ClientStatusOperation, ClientCollection
from src.domain.messages import EventClientDeleted, EventClientCantDeleted
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(dc: DataClient, uow: AbstractUnitOfWork) -> ClientCollection:
    with uow:
        client = Client(client_id=dc.client_id, name=dc.name, status=ClientStatusOperation.by_enable(dc.enable))

        client_collection=uow.client_collection_repository.get()

        client = client_collection.put_client(client=client)
        if type(client) is not Client:
            return client_collection

        uow.client_collection_repository.save(client_collection=client_collection)
        uow.events+=client_collection.events
        client_collection.events.clear()
        uow.commit()
        return client_collection


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    return uow.view_clients.get_client(client_id=client_id)


def list_clients(uow: AbstractUnitOfWork) -> list[ClientView]:
    return uow.view_clients.get_all_clients()


def delete_client(client_id: int, uow: AbstractUnitOfWork) -> bool:
    with uow:
        client_collection=uow.client_collection_repository.get()
        if client_collection.delete_id(client_id=client_id) and uow.client_collection_repository.delete(client_id=client_id):
            uow.events += client_collection.events
            client_collection.events=[]
        else:
            uow.events += client_collection.events
            client_collection.events = []
            return False

        uow.commit()
    return True
