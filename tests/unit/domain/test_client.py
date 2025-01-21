from src.domain.client import Client, ClientWrong, ClientAlreadyExists
from src.domain.status import ClientStatusEnabled, ClientStatusDisabled


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
    client=Client(client_id=1, name="Test Client",status=ClientStatusEnabled())
    assert type(client) is Client
    client_wrong=ClientWrong()
    assert type(client_wrong) is ClientWrong
    assert client_wrong.name==""
    client_wrong = ClientWrong(name="name")
    assert client_wrong.name=="name"
    client_exists = ClientAlreadyExists.already_exists(client=client)
    assert client_exists==client
    empty_client=Client.empty_client()
    assert empty_client==0 and empty_client.name=="" and type(empty_client.status) is ClientStatusDisabled

