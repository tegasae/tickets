import sqlite3

import pytest

from src.domain.status import ClientStatusEnabled, UserStatusEnabled
from src.domain.ticket import User
from src.domain.client import Client


def create_db_sqlite(path=":memory:", schema="../data/schema.sql"):
    with open(schema) as f:
        s = f.read()

    con = sqlite3.connect(path)
    con.executescript(s)
    cur = con.cursor()
    cur.execute("DELETE FROM clients")
    cur.execute("INSERT INTO clients (client_id,name,is_active) VALUES(1,'client1',1)")
    #cur.execute("INSERT INTO users (user_id,client_id,name,is_active) VALUES(10,1,'user1',1)")

    con.commit()
    return con


@pytest.fixture
def create_conn():
    con = create_db_sqlite()
    yield con
    con.close()


def get_client():
    return Client(client_id=1, name="client1", status=ClientStatusEnabled())


@pytest.fixture
def get_user(create_conn):
    cur = create_conn.cursor()
    cur.execute("INSERT INTO users (user_id,client_id,name,is_active) VALUES(1,1,'user1',1)")
    return User(user_id=1, client=get_client(), name="user1", status=UserStatusEnabled())
