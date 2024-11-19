import datetime

import pytest

from src.adapters.repositories.sqlite import SQLiteRepositoryTicket
from src.domain.exceptions import TicketNotFound
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed, TicketStatusCancelledUser
from src.domain.ticket import Ticket


def test_add_new_ticket(create_conn):
    date = datetime.datetime.now()
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(date=date, comment="comment"),
                                                   TicketStatusConfirmed(date=date, comment="comment")])
    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    assert ticket.ticket_id == 1
    cur = create_conn.cursor()
    cur.execute("SELECT ticket_id,describes FROM tickets WHERE ticket_id=1")
    r = cur.fetchone()
    assert r[0] == 1
    assert r[1] == ticket.describe
    cur.execute("SELECT status_ticket_id,date_,comment FROM ticket_status WHERE ticket_id=1")
    record = cur.fetchall()
    assert len(record) == 2
    assert record[0][0] == 2
    assert record[0][1] == date.isoformat()
    assert record[0][2] == "comment"


def test_update_ticket(create_conn):
    date = datetime.datetime.now()
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(date=date, comment="comment"),
                                                   TicketStatusConfirmed(date=date, comment="comment")])

    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    ticket.describe = "123"
    ticket.cancelled_by_user(comment="cancel")
    tr.save(user_id=1, ticket=ticket)
    cur = create_conn.cursor()
    cur.execute("SELECT ticket_id,describes FROM tickets WHERE ticket_id=1")
    r = cur.fetchone()
    assert r[0] == 1
    assert r[1] == ticket.describe
    cur.execute("SELECT status_ticket_id,date_,comment FROM ticket_status WHERE ticket_id=1")
    record = cur.fetchall()
    assert len(record) == 3


def test_update_not_exists(create_conn):
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(comment="comment"),
                                                   TicketStatusConfirmed(comment="comment")])

    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    ticket.ticket_id = 10
    with pytest.raises(TicketNotFound):
        tr.save(user_id=1, ticket=ticket)

def test_delete_ticket(create_conn):
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(comment="comment"),
                                                   TicketStatusConfirmed(comment="comment")])

    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    tr.delete(user_id=1,ticket_id=1)
    ticket.ticket_id=0
    tr.save(user_id=1, ticket=ticket)
    with pytest.raises(TicketNotFound):
        tr.delete(user_id=1, ticket_id=10)