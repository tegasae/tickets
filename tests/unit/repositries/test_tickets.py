import datetime

import pytest

from src.adapters.repositories.sqlite import SQLiteRepositoryTicket
from src.adapters.repository import _RepositoryStatus
from src.domain.exceptions import TicketNotFound
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed, TicketStatusCancelledUser, TicketStatus
from src.domain.ticket import Ticket


def test_add_new_ticket(create_conn):
    date = datetime.datetime.now()
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(date=date, comment="comment"),
                                                   TicketStatusConfirmed(date=date, comment="comment")])

    ticket1 = Ticket(describe="describe", statuses=[TicketStatusAccepted(date=date, comment="comment"),
                                                   TicketStatusConfirmed(date=date, comment="comment")])

    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    tr.save(user_id=1, ticket=ticket1)

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

    cur.execute("SELECT count(ticket_id) FROM tickets WHERE user_id=1")
    r = cur.fetchone()
    assert r[0]==2


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

def test_delete_ticket(create_conn):
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(comment="comment"),
                                                   TicketStatusConfirmed(comment="comment")])

    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    tr.delete(user_id=1,ticket_id=1)
    ticket.ticket_id=0
    tr.save(user_id=1, ticket=ticket)

def test_get_tickets(create_conn):
    date = datetime.datetime.now()
    ticket = Ticket(describe="describe", statuses=[TicketStatusAccepted(date=date, comment="comment"),
                                                   TicketStatusConfirmed(date=date, comment="comment")])

    ticket1 = Ticket(describe="describe", statuses=[TicketStatusAccepted(date=date, comment="comment"),
                                                    TicketStatusConfirmed(date=date, comment="comment")])

    tr = SQLiteRepositoryTicket(conn=create_conn)
    tr.save(user_id=1, ticket=ticket)
    tr.save(user_id=1, ticket=ticket1)
    tickets=tr.get(user_id=1)
    assert len(tickets)==2
    assert tickets[0].ticket_id==1
    assert type(tickets[1].statuses[0])==TicketStatusAccepted
    assert type(tickets[1].statuses[-1]) == TicketStatusConfirmed

def test_unknown_status():
    class T(TicketStatus):
        name="unknown"
    t=_RepositoryStatus.get_id_by_status(T)
    assert t==1