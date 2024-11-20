from src.domain.status import UserStatusEnabled
from src.domain.ticket import User
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

from tests.conftest import get_client


def test_commit(create_conn):
    uow = SQLLiteUnitOfWork(connection=create_conn)
    with uow:
        user = User(user_id=0, name='user',
                    client=get_client(),
                    status=UserStatusEnabled())
        uow.users.save(user=user)
        uow.commit()

    with uow:
        user1 = uow.users.get(user_id=1)
        uow.commit()

    assert user.user_id == user1.user_id
    assert user.name == user1.name


def test_rollback(create_conn):
    uow = SQLLiteUnitOfWork(connection=create_conn)
    try:
        with uow:
            user=User(user_id=0,name='user',
                                client=get_client(),
                                status=UserStatusEnabled())
            uow.users.save(user=user)
        raise Exception()
    except:
        user=uow.users.get(user_id=1)
        assert user.user_id==0

