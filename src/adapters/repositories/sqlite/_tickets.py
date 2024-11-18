import sqlite3

from src.adapters.repositories.sqlite._statues import _StoreStatus
from src.adapters.repository import AbstractRepositoryTicket
from src.domain.ticket import Ticket


class SQLiteRepositoryTicket(AbstractRepositoryTicket):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn=conn


    def _get_tickets(self,user_id:int):
        tickets: [Ticket] = []
        cursor=self.conn.cursor()
        select_tickets = (
            "select t.ticket_id, t.describes, st.status_ticket_id, st.status_ticket,ts.date_, ts.comment  "
            "FROM tickets "
            "t LEFT JOIN ticket_status ts ON t.ticket_id = ts.ticket_id LEFT JOIN statuses_ticket st ON "
            "ts.status_ticket_id = st.status_ticket_id  WHERE t.user_id =:user_id ORDER BY t.ticket_id, "
            "ts.date_")

        cursor.execute(select_tickets, {'user_id': user_id})
        records = cursor.fetchall()
        ticket_id = 0

        for r in records:
            ts= _StoreStatus.create_status(r[2], r[4], r[5])
            if r[0] != ticket_id:
                t = Ticket(ticket_id=r[0], describe=r[1], statuses=[ts])
                tickets.append(t)
                ticket_id = r[0]
                continue
            tickets[-1].statuses.append(ts)

        return tickets


    def _save_ticket(self, user_id: int, ticket: Ticket) -> Ticket:
        cursor=self.conn.cursor()
        count=0
        if not ticket.ticket_id:
            cursor.execute("INSERT INTO tickets (user_id,describes) VALUES (:user_id,:describes)",
                           {'user_id':user_id,'describes':ticket.describe})
            ticket.ticket_id=cursor.lastrowid
        else:
            count= _StoreStatus.count_statues(cursor=cursor, ticket_id=ticket.ticket_id)
        _StoreStatus.store_status(cursor, ticket.ticket_id, ticket.statuses[count:])
        return ticket


    def _delete(self, user_id: int, ticket_id: int)->bool:
        cursor=self.conn.cursor()
        _StoreStatus.delete_statues(cursor=cursor, ticket_id=ticket_id)
        cursor.execute("DELETE FROM tickets WHERE user_id=:user_id AND ticket_id=:ticket_id",
                       {'user_id':user_id,'ticket_id':ticket_id})
        return bool(cursor.rowcount)
