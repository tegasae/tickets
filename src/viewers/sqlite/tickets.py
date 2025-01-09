import sqlite3

from src.domain.status import get_status_by_id
from src.viewers.data import TicketView, ListTicketView, StatusView
from src.viewers.tickets import AbstractTicketViewer


class SQLiteTicketViewer(AbstractTicketViewer):

    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn

    @staticmethod
    def get_select(ticket_set: bool = False):
        if ticket_set:
            ticket_select = " AND t.ticket_id=:ticket_id "
        else:
            ticket_select = ""
        part_of_select = (f"select t.ticket_id, t.describes, ts.status_ticket_id,ts.date_, ts.comment FROM tickets t "
                          f"LEFT JOIN ticket_status ts ON t.ticket_id = ts.ticket_id "
                          f"WHERE t.user_id = :user_id  {ticket_select} ORDER BY t.ticket_id, ts.date_")

        return part_of_select

    def get_all_tickets_user(self, user_id: int) -> ListTicketView:
        cursor = self.conn.cursor()
        cursor.execute(self.get_select(), {'user_id': user_id})
        records = cursor.fetchall()
        ticket_id = 0
        ltv = ListTicketView()
        for r in records:

            ts = get_status_by_id(r[2])
            sv = StatusView(id=r[2], name=ts.name, date=r[3], comment=r[4])
            if r[0] != ticket_id:
                tv = TicketView(ticket_id=r[0], describe=r[1], statuses=[sv])
                ltv.list_tickets.append(tv)
                ticket_id = r[0]
                continue
            ltv.list_tickets[-1].statuses.append(sv)
        return ltv

    def get_ticket(self, user_id: int, ticket_id: int) -> TicketView:
        cursor = self.conn.cursor()

        cursor.execute(self.get_select(ticket_set=True), {'user_id': user_id, 'ticket_id': ticket_id})
        records = cursor.fetchall()
        if len(records) == 0:
            return TicketView(ticket_id=0, describe="", statuses=[])

        statuses = []
        r = ()
        for r in records:
            ts = get_status_by_id(r[2])
            sv = StatusView(id=r[2], name=ts.name, date=r[3], comment=r[4])
            statuses.append(sv)

        tv = TicketView(ticket_id=r[0], describe=r[1], statuses=statuses)
        return tv
