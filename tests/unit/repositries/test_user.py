from src.adapters.repository_sqlite import SQLiteRepositoryUser
from src.domain.status import ClientStatusEnabled, UserStatusEnabled, UserStatusDisabled
from src.domain.ticket import Client, User


def get_client():
    return Client(client_id=1, name="client1", status=ClientStatusEnabled())


# тест создания пользователя
def test_create_user(create_conn):
    ur = SQLiteRepositoryUser(conn=create_conn)
    user = User(user_id=0, name="user1", client=get_client(), status=UserStatusDisabled())
    ur.save(user=user)
    create_conn.commit()

    cur = create_conn.cursor()
    cur.execute("SELECT user_id,client_id,name,is_active FROM users WHERE user_id=1")
    r = cur.fetchone()
    print(type(user.status))
    print(r)
    assert user.user_id == r[0] and r[0] == 1
    assert user.client.client_id == r[1] and r[1] == 1
    assert user.name == r[2] and r[2] == "user1"
    assert type(user.status) is UserStatusDisabled and r[3]==0

# тест смены данных пользователя
def test_update_user(create_conn):
    ur = SQLiteRepositoryUser(conn=create_conn)
    cur=create_conn.cursor()
    cur.execute("INSERT INTO users (user_id,client_id,name,is_active) VALUES(1,1,'user1',1)")

    user = User(user_id=1, name="user2", client=get_client(), status=UserStatusEnabled())
    ur.save(user=user)
    create_conn.commit()

    cur = create_conn.cursor()
    cur.execute("SELECT user_id,client_id,name,is_active FROM users WHERE user_id=1")
    r = cur.fetchone()
    print(type(user.status))
    print(r)
    assert user.user_id == r[0] and r[0] == 1
    assert user.client.client_id == r[1] and r[1] == 1
    assert user.name == r[2] and r[2] == "user2"
    assert type(user.status) is UserStatusEnabled and r[3]==1



# тест удаления пользователя
