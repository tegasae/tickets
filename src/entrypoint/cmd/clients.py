from src.api.cmd.cmd import command_wrapper
from src.api.cmd.descriptor import CommandInt, CommandJSON
from src.domain.input_data import DataClient
from src.services.service_layer.client import get_client, list_clients, create_client


@command_wrapper(name="list_client", descriptor=CommandInt)
def list_client(argument: CommandInt) -> str:
    print('list of clients')
    if argument.arg:
        c=get_client(client_id=argument.arg, uow=argument.addition['uow'])
        if c.id==0:
            return "not found"
        return str(c)
    else:
        clients=list_clients(uow=argument.addition['uow'])
        if len(clients)==0:
            return "not found"
        return str(clients)

@command_wrapper(name="add_client", descriptor=CommandJSON)
def create(argument: CommandJSON)->str:
    dc=DataClient(client_id=0,name=argument.arg['name'],status=argument.arg['status'])
    client=create_client(dc=dc,uow=argument.addition['uow'])
    if client.client_id==0:
        return "Don't create"
    return str(client.client_id)