from src.domain.exceptions import ClientCantCreate
from src.domain.input_data import DataClient
from src.domain.status import ClientStatusOperation
from src.domain.ticket import Client
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def save_client(dc: DataClient,uow:AbstractUnitOfWork)->Client:
    with uow:
        status=ClientStatusOperation.by_enable(dc.enable)
        if uow.view_clients.client_exists_by_name(dc.name):
            return Client(client_id=0,name=dc.name,status=status)
        client=Client(client_id=dc.client_id,name=dc.name,status=status)
        client=uow.clients.save(client=client)
        if client.client_id==0:
            return Client(client_id=0,name=dc.name,status=status)
        uow.commit()
        return client


def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    tc = uow.view_clients.get_client(client_id=client_id)
    return tc

def list_clients(uow:AbstractUnitOfWork)->list[ClientView]:
   return uow.view_clients.get_all_clients()

def delete_client(client_id:int, uow:AbstractUnitOfWork)->bool:
    return uow.clients.delete(client_id=client_id)