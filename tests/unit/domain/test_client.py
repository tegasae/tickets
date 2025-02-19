from src.domain.client import Client, ClientWrong, ClientCollection, ClientEmpty, ClientStatus, \
    ClientStatusEnabled, ClientStatusDisabled, ClientStatusOperation




def test_client():
    client = Client(client_id=1, name="Test Client", status=ClientStatusEnabled(),code="code")
    assert type(client) is Client

    client_wrong = ClientWrong()
    assert type(client_wrong) is ClientWrong and client_wrong.name == ""


    empty_client = ClientEmpty()
    assert empty_client.client_id == 0 and empty_client.name == "" and type(empty_client.status) is ClientStatusDisabled



def test_client_collect():
    # создаем коллекцию
    client_collect = ClientCollection(clients=[Client(client_id=1,name="name1",code="code1",status=ClientStatusEnabled())])
    client=Client(client_id=0,name="name0",code="code0",status=ClientStatusEnabled())
    client=client_collect.put_client(client)
    assert client.client_id==0 and len(client_collect.by_code)==2
    assert len(client_collect.get_clients())==2

    client=ClientEmpty()
    client=client_collect.put_client(client)
    assert type(client) is ClientWrong and len(client_collect.by_code) == 2

    client = Client(name="      ",code="",client_id=0)
    client = client_collect.put_client(client)
    assert type(client) is ClientWrong and len(client_collect.by_code) == 2


    client=client_collect.disable(client_id=1)
    assert type(client.status) is ClientStatusDisabled
    client = client_collect.disable(client_id=10)
    assert type(client) is ClientEmpty

    client = client_collect.enable(client_id=1)
    assert type(client.status) is ClientStatusEnabled
    client = client_collect.enable(client_id=10)
    assert type(client) is ClientEmpty

    client_collect.put_client(Client(client_id=10,name="name10",code="code10"))
    r=client_collect.delete_id(client_id=10)
    assert r is True and len(client_collect.by_code)==2


    r = client_collect.delete_id(client_id=10)
    assert r is False and len(client_collect.by_code) == 2


def test_client_status():
    client_enabled = ClientStatusOperation.by_id(1)
    assert type(client_enabled) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_id(10)) is ClientStatus

    assert ClientStatusOperation.by_type(ClientStatusEnabled) == 1
    assert ClientStatusOperation.by_type(list) == 0

    assert type(ClientStatusOperation.by_enable(True)) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_enable(False)) is ClientStatusDisabled
