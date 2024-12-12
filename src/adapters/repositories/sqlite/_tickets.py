import datetime
import sqlite3

from src.adapters.repository import AbstractRepositoryTicket, _RepositoryStatus
from src.domain.ticket import Ticket


class SQLiteRepositoryTicket(AbstractRepositoryTicket):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn

    def _get(self, user_id: int):
        tickets: [Ticket] = []
        cursor = self.conn.cursor()
        select_tickets = ("select t.ticket_id, t.describes, ts.status_ticket_id,ts.date_, ts.comment FROM tickets t "
                          "LEFT JOIN ticket_status ts ON t.ticket_id = ts.ticket_id "
                          "WHERE t.user_id = :user_id ORDER BY t.ticket_id, ts.date_")
        cursor.execute(select_tickets, {'user_id': user_id})
        records = cursor.fetchall()
        ticket_id = 0

        for r in records:

            ts = _RepositoryStatus.get_status_by_id(r[2])
            print(ts)
            s = ts(date=datetime.datetime.fromisoformat(r[3]),comment=r[4])

            if r[0] != ticket_id:
                t = Ticket(ticket_id=r[0], describe=r[1], statuses=[s])
                tickets.append(t)
                ticket_id = r[0]
                continue
            tickets[-1].statuses.append(s)
        return tickets

    def _save(self, user_id: int, ticket: Ticket) -> Ticket:
        cursor = self.conn.cursor()
        count=0
        if not ticket.ticket_id:
            cursor.execute("INSERT INTO tickets (user_id,describes) VALUES (:user_id,:describes)",
                           {'user_id': user_id, 'describes': ticket.describe})
            ticket.ticket_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE tickets SET user_id=:user_id, describes=:describe WHERE ticket_id=:ticket_id",
                           {"user_id":user_id,'describe':ticket.describe,'ticket_id':ticket.ticket_id})
            if cursor.rowcount==0:
                ticket.ticket_id=0
                return ticket
            cursor.execute("SELECT count(status_ticket_id) FROM ticket_status WHERE ticket_id=:ticket_id",
                           {'ticket_id': ticket.ticket_id})
            r = cursor.fetchone()
            count = r[0]
        for t in ticket.statuses[count:]:
            cursor.execute("INSERT INTO ticket_status (ticket_id,status_ticket_id,date_,comment) "
                           "VALUES(:ticket_id,:status_ticket_id,:date,:comment)",
                           {'ticket_id': ticket.ticket_id,
                            'status_ticket_id': _RepositoryStatus.get_id_by_status(t),
                            'date': t.date.isoformat(),
                            'comment': t.comment})
        return ticket

    def _delete(self, user_id: int, ticket_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM ticket_status WHERE ticket_id=:ticket_id", {'ticket_id': ticket_id})
        cursor.execute("DELETE FROM tickets WHERE user_id=:user_id AND ticket_id=:ticket_id",
                       {'user_id': user_id, 'ticket_id': ticket_id})
        return bool(cursor.rowcount)
