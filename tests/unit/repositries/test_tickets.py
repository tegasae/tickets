from src.adapters.repositories.sqlite import SQLiteRepositoryTicket
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed, TicketStatusCancelledUser
from src.domain.ticket import Ticket


def test_save_ticket(create_conn):
    tr = SQLiteRepositoryTicket(conn=create_conn)
    ticket=Ticket(describe="123",statuses=[TicketStatusAccepted(),TicketStatusConfirmed()])
    tr.save(user_id=1, ticket=ticket)
    assert ticket.ticket_id==1
    assert type(ticket.statuses[0]) is TicketStatusAccepted
    assert type(ticket.statuses[1]) is TicketStatusConfirmed
    cur=create_conn.cursor()
    cur.execute("SELECT ticket_id, user_id, describes FROM tickets WHERE ticket_id=1")
    r=cur.fetchone()
    assert ticket.ticket_id==r[0]
    assert r[1]==1
    assert ticket.describe==r[2]
    cur.execute("SELECT ticket_id, status_ticket_id FROM ticket_status WHERE ticket_id=1")
    record=cur.fetchall()
    for r in record:
        assert r[0]==1
    assert len(record)==2
    assert r[1]==3





def test_get_tickets(create_conn):
    tr = SQLiteRepositoryTicket(conn=create_conn)
    ticket= Ticket(describe="123", statuses=[TicketStatusAccepted(), TicketStatusConfirmed()])
    tr.save(user_id=1, ticket=ticket)
    ticket = Ticket(describe="123", statuses=[TicketStatusAccepted(), TicketStatusCancelledUser(comment="123")])
    tr.save(user_id=1, ticket=ticket)

    tickets = tr.get(user_id=1)
    assert len(tickets)==2

def test_change_ticket(create_conn):
    tr = SQLiteRepositoryTicket(conn=create_conn)
    ticket = Ticket(describe="123", statuses=[TicketStatusAccepted(), TicketStatusConfirmed()])
    tr.save(user_id=1, ticket=ticket)
    tickets = tr.get(user_id=1)
    assert len(tickets[0].statuses)==2

    ticket.cancelled_by_user(comment="cancel")
    tr.save(user_id=1,ticket=ticket)
    tickets = tr.get(user_id=1)
    assert len(tickets[0].statuses) == 3
    assert type(tickets[0].active_status) is TicketStatusCancelledUser

def test_change_not_exist_ticket(create_conn):
    tr = SQLiteRepositoryTicket(conn=create_conn)
    ticket = Ticket(describe="123", statuses=[TicketStatusAccepted(), TicketStatusConfirmed()])
    tr.save(user_id=1, ticket=ticket)
    tickets = tr.get(user_id=1)
    assert len(tickets[0].statuses)==2

    ticket.cancelled_by_user(comment="cancel")
    ticket.ticket_id=2
    tr.save(user_id=1,ticket=ticket)
    tickets = tr.get(user_id=1)
    assert len(tickets[0].statuses) == 3
    assert type(tickets[0].active_status) is TicketStatusCancelledUser

