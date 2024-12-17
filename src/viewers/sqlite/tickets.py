import sqlite3

from src.domain.status import get_status_by_id
from src.viewers.data import TicketView, ListTicketView, StatusView
from src.viewers.tickets import AbstractTicketViewer


class SQLiteTicketViewer(AbstractTicketViewer):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn

    def get_all_tickets(self, user_id: int) -> ListTicketView:
        cursor = self.conn.cursor()
        select_tickets = (
            "select t.ticket_id, t.describes, ts.status_ticket_id,ts.date_, ts.comment FROM tickets t "
            "LEFT JOIN ticket_status ts ON t.ticket_id = ts.ticket_id "
            "WHERE t.user_id = :user_id ORDER BY t.ticket_id, ts.date_")
        cursor.execute(select_tickets, {'user_id': user_id})
        records = cursor.fetchall()
        ticket_id = 0
        ltv=ListTicketView()
        for r in records:

            ts = get_status_by_id(r[2])
            sv=StatusView(id=r[2],name=ts.name,date=r[3],comment=r[4])
            if r[0] != ticket_id:
                tv = TicketView(ticket_id=r[0], describe=r[1], statuses=[sv])
                ltv.list_tickets.append(tv)
                ticket_id = r[0]
                continue
            ltv.list_tickets[-1].statuses.append(sv)
        return ltv

