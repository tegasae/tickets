
from src.api.cmd.cmd import command_wrapper
from src.api.cmd.descriptor import CommandInt, CommandJSON
from src.domain.client import Client, ClientAlreadyExists
from src.domain.input_data import DataClient
from src.services.service_layer.client import get_client, list_clients, save_client, delete_client


@command_wrapper(name="list_client", descriptor=CommandInt)
def list_client(argument: CommandInt) -> str:
    print('list of clients')
    if argument.arg:
        c = get_client(client_id=argument.arg, uow=argument.addition['uow'])
        if c.id == 0:
            return f"The client with id={argument.arg} didn't find"
        return str(c)
    else:
        clients = list_clients(uow=argument.addition['uow'])
        if len(clients) == 0:
            return "The clients didn't find"
        return str(clients)


def save(argument: CommandJSON) -> str:
    status: bool = False
    try:
        if str(argument.arg['enable']).lower() == "true":
            status = True
        dc = DataClient(client_id=argument.arg['id'], name=argument.arg['name'], enable=status)
        client = save_client(dc=dc, uow=argument.addition['uow'])
        if type(client) is Client:
            return str(client.client_id)
        if type(client) is ClientAlreadyExists:
            return f"The {argument.arg['name']} is already exsited."
        return f"The {argument.arg['name']} isn't stored."
    except ValueError:
        return "The data is wrong"


@command_wrapper(name="add_client", descriptor=CommandJSON)
def create(argument: CommandJSON) -> str:
    argument.arg['id'] = 0
    return save(argument)


@command_wrapper(name="change_client", descriptor=CommandJSON)
def change(argument: CommandJSON) -> str:
    return save(argument)


@command_wrapper(name="delete_client", descriptor=CommandInt)
def delete(argument: CommandInt):
    if argument.arg:
        deleted = delete_client(client_id=argument.arg, uow=argument.addition['uow'])
        if deleted:
            return f"The client {argument.arg} is deleted."
        else:
            return f"The client {argument.arg} isn't deleted."
