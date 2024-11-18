import sqlite3
from datetime import datetime

from src.adapters.repositories.sqlite._statues import _StoreStatus
from src.adapters.repositories.sqlite._users import SQLiteRepositoryUser
from src.domain.status import ClientStatusEnabled, UserStatusDisabled, TicketStatusAccepted, TicketStatusConfirmed
from src.domain.ticket import Client, User, Ticket

if __name__ == "__main__":
    tick: [Ticket]
    connect = sqlite3.connect(database="../../data/tickets.db")
    s = SQLiteRepositoryUser(conn=connect)
    cursor = connect.cursor()
    date = datetime.now()
    statues = [TicketStatusAccepted(date=date), TicketStatusConfirmed(date=date, comment="comment")]
    _StoreStatus.store_status(cursor=cursor, ticket_id=1, statuses=statues)
    cursor.execute("SELECT ticket_id,status_ticket_id,date_,comment FROM ticket_status")
    result = cursor.fetchall()
    count = 0
    r = ()
    for r in result:
        count += 1

    assert r[0] == 1
    print(r)
    print("-------------------")
    status = _StoreStatus.create_status(status_id=r[1], date=r[2], comment=r[3])
    assert status.date == date
