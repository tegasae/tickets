import datetime

from src.adapters.repositories.sqlite._statues import _StoreStatus
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed, TicketStatus


#def test_get_status():
#    assert _StoreStatus.get_status(TicketStatusConfirmed())==3

def test_save_status(create_conn):
    cursor=create_conn.cursor()
    date=datetime.datetime.now()
    statues=[TicketStatusAccepted(date=date),TicketStatusConfirmed(date=date,comment="comment")]
    _StoreStatus.store_status(cursor=cursor,ticket_id=1,statuses=statues)
    cursor.execute("SELECT ticket_id,status_ticket_id,date_,comment FROM ticket_status")
    result=cursor.fetchall()
    count=0
    r=()
    for r in result:
        count+=1
    assert count==2
    assert _StoreStatus.count_statues(cursor=cursor,ticket_id=1)==2
    assert r[0]==1

    status=_StoreStatus.create_status(status_id=r[1],date=r[2],comment=r[3])
    assert status.date==date
    _StoreStatus.delete_statues(cursor=cursor,ticket_id=1)
    assert _StoreStatus.count_statues(cursor=cursor, ticket_id=1) == 0

def test_status_not_found():
    class NewStatus(TicketStatusAccepted):
        comment = "123"

    i=_StoreStatus.get_status(NewStatus())
    assert i is TicketStatus