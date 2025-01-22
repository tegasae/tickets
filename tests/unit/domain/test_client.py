from src.domain.client import Client, ClientWrong, ClientAlreadyExists, ClientsCollect
from src.domain.status import ClientStatusEnabled, ClientStatusDisabled, ClientStatusOperation, ClientStatus


def test_client_is_active():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    assert client.is_active() is True
    client.disable()
    assert client.is_active() is False
    client.enable()
    assert client.is_active() is True


def test_client_is_not_active():
    client = Client(client_id=1, name="Test Client", status=ClientStatusDisabled())
    assert client.is_active() is False


def test_client_create():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled())
    assert type(client) is Client
    client_wrong = ClientWrong()
    assert type(client_wrong) is ClientWrong
    assert client_wrong.name == ""
    client_wrong = ClientWrong(name="name")
    assert client_wrong.name == "name"
    client_exists = ClientAlreadyExists.already_exists(client=client)
    assert client_exists == client
    empty_client = Client.empty_client()
    assert empty_client.client_id == 0 and empty_client.name == "" and type(empty_client.status) is ClientStatusDisabled


def test_client_collect():
    client_collect = ClientsCollect(clients=[Client(client_id=1, name="name", status=ClientStatusEnabled())])

    client1 = client_collect.create_client(client_id=1, name="name1", status=ClientStatusEnabled())
    assert type(client1) is Client and client1.client_id == 1 and client1.name == "name1"
    client_exists = client_collect.create_client(client_id=1, name="name1", status=ClientStatusEnabled())
    assert type(client_exists) is ClientAlreadyExists and client1.name == "name1"
    client_collect_empty = ClientsCollect()
    assert type(client_collect_empty.clients) is list
    client_wrong = client_collect_empty.create_client(name="      ")
    assert type(client_wrong) is ClientWrong


def test_client_status():
    client_enabled = ClientStatusOperation.by_id(1)
    assert type(client_enabled) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_id(10)) is ClientStatus

    assert ClientStatusOperation.by_type(ClientStatusEnabled) == 1
    assert ClientStatusOperation.by_type(list) == 0

    assert type(ClientStatusOperation.by_enable(True)) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_enable(False)) is ClientStatusDisabled
