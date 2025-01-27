from src.domain.client import Client, ClientWrong, ClientAlreadyExists, ClientsCollect, ClientEmpty, ClientStatus, \
    ClientStatusEnabled, ClientStatusDisabled, ClientStatusOperation


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
    # создаем коллекцию
    client_collect = ClientsCollect()

    #пытаемся поместить в коллекскию не Client
    client_emmty=client_collect.put_client(ClientEmpty())
    assert type(client_emmty) is ClientEmpty


    #пытаемся поместить в коллекскию клиента с пустым именем
    client_wrong=client_collect.put_client(Client(client_id=1, name='   ', status=ClientStatusEnabled()))
    assert type(client_wrong) is ClientWrong and client_wrong.name=='   '

    #помещаем в коллеккцию клиента с id=0
    client=client_collect.put_client(Client(client_id=0, name='name', status=ClientStatusEnabled()))
    assert type(client) is Client and len(client_collect.by_name) == 1 and len(client_collect.by_id)==0

    # меняем статус клиент
    client = client_collect.put_client(Client(client_id=0, name='name', status=ClientStatusDisabled()))
    assert type(client) is Client and len(client_collect.by_name) == 1 and len(client_collect.by_id) == 0 \
            and type(client.status) is ClientStatusDisabled

    #присваимваем id=1
    client=client_collect.put_client(Client(client_id=1, name='name', status=ClientStatusEnabled()))

    assert type(client) is Client and len(client_collect.by_name) == 1 and len(client_collect.by_id)==1 \
            and client.client_id==1 and type(client.status) is ClientStatusEnabled

    #добавляем еще клиента с id=1
    client = client_collect.put_client(Client(client_id=2, name='name 2', status=ClientStatusEnabled()))

    assert type(client) is Client and len(client_collect.by_name) == 2 and len(client_collect.by_id) == 2 \
           and client.client_id == 2 and type(client.status) is ClientStatusEnabled

    # добавляем клиента с существуюшим именем
    client = client_collect.put_client(Client(client_id=3, name='name', status=ClientStatusEnabled()))
    assert type(client) is ClientAlreadyExists and len(client_collect.by_name) == 2 and len(client_collect.by_id) == 2

    # меняем статус у клиента
    client = client_collect.put_client(Client(client_id=2, name='name 2', status=ClientStatusDisabled()))
    assert type(client) is Client and len(client_collect.by_name) == 2 and len(client_collect.by_id) == 2 \
           and client.client_id == 2 and type(client.status) is ClientStatusDisabled

    # менем имя у клиента
    client = client_collect.put_client(Client(client_id=2, name='name 3', status=ClientStatusEnabled()))
    assert type(client) is Client and len(client_collect.by_name) == 2 and len(client_collect.by_id) == 2 \
           and client.client_id == 2 and client_collect.by_id[2].name=='name 3' and type(client.status) is ClientStatusEnabled

    # добавляем клиента id=0 с существующим именем
    client = client_collect.put_client(Client(client_id=0, name='name 3', status=ClientStatusEnabled()))
    assert type(client) is ClientAlreadyExists


    # добавлеяем нового клиента с id=0
    client1 = Client(client_id=0, name="new client", status=ClientStatusEnabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is Client and len(client_collect.by_name) == 3

    r = client_collect.delete_id(client_id=1)
    assert r == True and len(client_collect.by_name) == 2

    r = client_collect.delete_id(client_id=1)
    assert r == False

    r=client_collect.delete_name(name='new client')
    assert r==True

    r = client_collect.delete_name(name='new client')
    assert r == False

def test_client_status():
    client_enabled = ClientStatusOperation.by_id(1)
    assert type(client_enabled) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_id(10)) is ClientStatus

    assert ClientStatusOperation.by_type(ClientStatusEnabled) == 1
    assert ClientStatusOperation.by_type(list) == 0

    assert type(ClientStatusOperation.by_enable(True)) is ClientStatusEnabled
    assert type(ClientStatusOperation.by_enable(False)) is ClientStatusDisabled
