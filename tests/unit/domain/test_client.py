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
    # создаем коллекцию с одним клиентом
    client_collect = ClientsCollect()
    client_collect = ClientsCollect()
    client_wrong=client_collect.put_client(Client(client_id=1, name='   ', status=ClientStatusEnabled()))
    assert type(client_wrong) is ClientWrong and client_wrong.name=='   '


    client_collect.put_client(Client(client_id=1, name='name', status=ClientStatusEnabled()))
    # пытаемся добавить неправильного клиента
    client_wrong = ClientWrong()
    client_wrong = client_collect.put_client(client_wrong)
    assert type(client_wrong) is ClientWrong and len(client_collect.by_name) == 1

    # добавлеяем нового клиента с id=0
    client1 = Client(client_id=0, name="new client", status=ClientStatusEnabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is Client and len(client_collect.by_name) == 2

    # добавляем нового клиента с id=0 и существущем именем
    client1 = Client(client_id=0, name="name", status=ClientStatusEnabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is ClientAlreadyExists and len(client_collect.by_name) == 2

    # обновляем клиента с id=0 сущуствуюещм именем и другим статусом
    client1 = Client(client_id=0, name="new client", status=ClientStatusDisabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is Client and len(client_collect.by_name) == 2 and type(client1.status) is ClientStatusDisabled

    ###########
    # клиент, которые уже есть, но id=0, обновляем с id!=0
    client1 = Client(client_id=10, name="new client", status=ClientStatusDisabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is Client and len(client_collect.by_name) == 2 and client1.name == 'new client' \
           and len(client_collect.by_id) == 2 and type(client1.status) is ClientStatusDisabled

    # клиент, который существует, обновляем статус
    client1 = Client(client_id=1, name="name", status=ClientStatusDisabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is Client and len(client_collect.by_name) == 2 and client1.name == 'name' \
           and client_collect.by_name[client1.name].client_id == client_collect.by_id[client1.client_id].client_id \
           and type(client_collect.by_name[client1.name].status) is ClientStatusDisabled

    # пробуем добавить нового клиента, с новым id, но сущестующим именемм
    client1 = Client(client_id=2, name="name", status=ClientStatusEnabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is ClientAlreadyExists and len(client_collect.by_name) == 2

    # обновляем имя клиента, с существующим id
    client1 = Client(client_id=1, name="name1", status=ClientStatusDisabled())
    client1 = client_collect.put_client(client1)
    assert type(client1) is Client and len(client_collect.by_name) == 2 and len(client_collect.by_id) == 2 \
           and client_collect.by_name['name1'].client_id == 1 and client_collect.by_id[1].name == 'name1' \
           and client_collect.by_name['name1'].status == client_collect.by_id[1].status \
           and type(client_collect.by_name['name1'].status) is ClientStatusDisabled

    r = client_collect.delete_id(client_id=1)
    assert r == True and len(client_collect.by_name) == 1

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
