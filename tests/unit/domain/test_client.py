from src.domain.client import Client, ClientWrong, ClientAlreadyExists, ClientsCollect, ClientEmpty
from src.domain.status import ClientStatusEnabled, ClientStatusDisabled, ClientStatusOperation, ClientStatus


def test_client_is_active():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    assert client.is_active() is True

    client.disable()
    assert client.is_active() is False

    client.enable()
    assert client.is_active() is True


def test_client():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    assert type(client) is Client

    client_wrong = ClientWrong()
    assert type(client_wrong) is ClientWrong and client_wrong.name == ""

    client_exists = ClientAlreadyExists.already_exists(client=client)
    assert client_exists.name == client.name

    empty_client = Client.empty_client()
    assert empty_client.client_id == 0 and empty_client.name == "" and type(empty_client.status) is ClientStatusDisabled

    empty_client = ClientEmpty()
    assert empty_client.client_id == 0 and empty_client.name == "" and type(empty_client.status) is ClientStatusDisabled


def test_client_create():
    client1 = ClientsCollect.create_client(client_id=1, name="name1", status=ClientStatusEnabled())
    assert type(client1) is Client and client1.client_id == 1 and client1.name == "name1"

    client_empty = ClientsCollect.create_client(client_id=1, name="  ", status=ClientStatusEnabled())
    assert type(client_empty) is ClientWrong and client_empty.name == '  '

    client2 = ClientsCollect.create_client(client_id=1, name=" n ", status=ClientStatusEnabled())
    assert type(client2) is Client and client2.client_id == 1 and client2.name == "n"




def test_client_collect():
    client_collect_empty = ClientsCollect()
    assert type(client_collect_empty.clients) is list

    client_collect = ClientsCollect(clients=[Client(client_id=1,name="name",status=ClientStatusEnabled())])
    client_wrong = ClientWrong()
    client_wrong=client_collect.put_client(client_wrong)
    assert type(client_wrong) is ClientWrong and len(client_collect.clients)==1

    client=Client(client_id=0,name="new client",status=ClientStatusEnabled())
    client=client_collect.put_client(client)
    assert type(client) is Client and len(client_collect.clients)==1

    client = Client(client_id=0, name="name", status=ClientStatusEnabled())
    client = client_collect.put_client(client)
    assert type(client) is ClientAlreadyExists and len(client_collect.clients) == 1


def test_client_status():
    client_enabled = ClientStatusOperation.by_id(1)
    assert type(client_enabled) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_id(10)) is ClientStatus

    assert ClientStatusOperation.by_type(ClientStatusEnabled) == 1
    assert ClientStatusOperation.by_type(list) == 0

    assert type(ClientStatusOperation.by_enable(True)) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_enable(False)) is ClientStatusDisabled
