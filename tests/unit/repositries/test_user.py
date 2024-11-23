import pytest

from src.adapters.repositories.sqlite import SQLiteRepositoryUser
from src.domain.exceptions import UserNotFound
from src.domain.status import UserStatusEnabled, UserStatusDisabled
from src.domain.ticket import User
from tests.conftest import get_client


# тест создания пользователя
def test_save_user(create_conn):
    ur = SQLiteRepositoryUser(conn=create_conn)
    user = User(user_id=0, name="user1", client=get_client(), status=UserStatusEnabled())
    ur.save(user=user)
    create_conn.commit()

    cur = create_conn.cursor()
    cur.execute("SELECT user_id,client_id,name,is_active FROM users WHERE user_id=1")
    r = cur.fetchone()

    assert user.user_id == r[0] and r[0] == 1
    assert user.client.client_id == r[1] and r[1] == 1
    assert user.name == r[2] and r[2] == "user1"
    assert type(user.status) is UserStatusEnabled and r[3] == 1

    user.name='user2'
    ur.save(user=user)

    cur.execute("SELECT user_id,client_id,name,is_active FROM users WHERE user_id=1")
    r = cur.fetchone()

    assert user.user_id == r[0] and r[0] == 1
    assert user.client.client_id == r[1] and r[1] == 1
    assert user.name == r[2] and r[2] == "user2"


def test_get_user(create_conn):
    cur = create_conn.cursor()
    cur.execute("INSERT INTO users (user_id,client_id,name,is_active) VALUES(1,1,'user1',1)")
    ur = SQLiteRepositoryUser(conn=create_conn)
    user = ur.get(user_id=1)
    assert user.user_id == 1
    assert user.client.client_id == 1
    assert user.name == 'user1'
    assert len(user.tickets) == 0
    assert type(user.status) is UserStatusEnabled
    user=ur.get(user_id=2)
    assert user.user_id==0





def test_delete_user(create_conn):
    user = User(user_id=0, name="name", client=get_client(), status=UserStatusEnabled())
    ur = SQLiteRepositoryUser(conn=create_conn)
    ur.save(user)
    assert len(ur.seen_users) == 1
    ur.delete(user_id=1)
    with pytest.raises(UserNotFound):
        ur.delete(user_id=1)

