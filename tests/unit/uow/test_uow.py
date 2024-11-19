from src.domain.status import ClientStatusEnabled, UserStatusEnabled
from src.domain.ticket import User, Client
from src.services.sqlite.unit_of_work import SqlAlchemyUnitOfWork


def test_commit(create_conn):
    uow=SqlAlchemyUnitOfWork(connection=create_conn)
    with uow:
        user=User(user_id=0,name='user',
                                      client=Client(client_id=1,name='client',status=ClientStatusEnabled()),
                            status=UserStatusEnabled())
        uow.users.save(user=user)
        uow.commit()


    with uow:
        user1=uow.users.get(user_id=1)
        uow.commit()

    assert user.user_id==user1.user_id
    assert user.name == user1.name


def test_rollback(create_conn):
    uow=SqlAlchemyUnitOfWork(connection=create_conn)
    create_conn.execute("INSERT INTO clients (client_id,name,is_active) VALUES (10,'client',1)")
    try:
        with uow:
            user=User(user_id=0,name='user',
                                      client=Client(client_id=10,name='client',status=ClientStatusEnabled()),
                                status=UserStatusEnabled())
            uow.users.save(user=user)
        raise Exception()
    except:
        user=uow.users.get(user_id=1)


