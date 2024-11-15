import sqlite3

import pytest

from src.adapters.repository_sqlite import SQLiteRepositoryUser


def create_db_sqlite(path=":memory:", schema="../data/schema.sql"):
    with open(schema) as f:
        s=f.read()

    con = sqlite3.connect(path)
    con.executescript(s)
    cur=con.cursor()
    cur.execute("DELETE FROM clients")
    cur.execute("INSERT INTO clients (client_id,name,is_active) VALUES(1,'client1',1)")
    con.commit()
    return con


@pytest.fixture
def create_conn():
    con = create_db_sqlite()
    yield con
    con.close()
