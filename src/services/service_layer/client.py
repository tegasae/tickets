from src.domain.exceptions import ErrorWithStore
from src.domain.client import Client, ClientStatusOperation, ClientCollection, ClientEmpty
from src.domain.messages import EventClientCreated, EventClientCantStored, CreateClient, ViewClient
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(cmd: CreateClient, uow: AbstractUnitOfWork) -> ClientCollection:
    with uow:
        try:
            client_collection = uow.client_collection.get()
            client = client_collection.create_client(client_id=0, name=cmd.name, code=cmd.code1s,
                                                     status=ClientStatusOperation.by_enable(cmd.enable))
            if type(client) is Client:
                client = uow.client_collection.add(client=client)
                client_collection.put_client(client=client)

            uow.events += client_collection.events
            client_collection.events.clear()
            uow.events.append(ViewClient())
            #messagebus.handle(EventClientCreated(client_id=client.client_id), uow)
            uow.commit()
        except ErrorWithStore:
            client_collection.delete_id(client_id=client.client_id)
            uow.events.append(EventClientCantStored())
    return client_collection


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    return uow.view_clients.get_client(client_id=client_id)


def list_clients(uow: AbstractUnitOfWork) -> list[ClientView]:
    return uow.view_clients.get_all_clients()


def delete_client(client_id: int, uow: AbstractUnitOfWork) -> bool:
    with uow:
        client_collection = uow.client_collection.get()
        if uow.client_collection.delete(client_id=client_id) and client_collection.delete_id(client_id=client_id):
            uow.events += client_collection.events
        else:
            uow.events += client_collection.events
            return False
        uow.commit()
    return True


def disable_client(client_id: int, uow: AbstractUnitOfWork) -> bool:
    with uow:
        client_collection = uow.client_collection.get()
        client = client_collection.disable(client_id=client_id)
        if type(client) is ClientEmpty:
            return False
        uow.client_collection.save(client_collection)
        uow.commit()
    return True
