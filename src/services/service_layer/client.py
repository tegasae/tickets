from src.domain.exceptions import ClientCantCreate
from src.domain.input_data import DataClient
from src.domain.ticket import Client
from src.services.unit_of_work import AbstractUnitOfWork
from src.viewers.data import ClientView


def create_client(dc: DataClient,uow:AbstractUnitOfWork)->Client:
    with uow:
        if uow.view_clients.client_exists_by_name(dc.name):
            return Client(client_id=0,name=dc.name,status=dc.status)
        client=Client(client_id=0,name=dc.name,status=dc.status)
        client=uow.clients.save(client=client)
        if client.client_id==0:
            return Client(client_id=0,name=dc.name,status=dc.status)
        uow.commit()
        return client

def get_client(client_id: int, uow: AbstractUnitOfWork) -> ClientView:
    tc = uow.view_clients.get_client(client_id=client_id)
    return tc

def list_clients(uow:AbstractUnitOfWork)->list[ClientView]:
   return uow.view_clients.get_all_clients()