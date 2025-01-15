
from src.domain.status import get_status_by_id
from src.utils.dbapi.connect import Connection
from src.viewers.data import TicketView, ListTicketView, StatusView
from src.viewers.tickets import AbstractTicketViewer


class SQLiteTicketViewer(AbstractTicketViewer):

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn





    def get_all_tickets(self, user_id: int) -> ListTicketView:
        ticket_id = 0
        ltv = ListTicketView()

        query=self.conn.create_query(
            f"select t.ticket_id, t.describes, ts.status_ticket_id,ts.date_, ts.comment FROM tickets t "
            f"LEFT JOIN ticket_status ts ON t.ticket_id = ts.ticket_id "
            f"WHERE t.user_id = :user_id  ORDER BY t.ticket_id, ts.date_",
            params={"user_id":user_id},
            var=["id","describe","status","date","comment"]
        )

        for r in query.get_result():
            ts = get_status_by_id(r["status"])
            sv = StatusView(id=r["status"], name=ts.name, date=r["date"], comment=r["comment"])
            if r["id"] != ticket_id:
                tv = TicketView(ticket_id=r["id"], describe=r["describe"], statuses=[sv])
                ltv.list_tickets.append(tv)
                ticket_id = r["id"]
                continue
            ltv.list_tickets[-1].statuses.append(sv)
        return ltv

    def get_ticket(self, user_id: int, ticket_id: int) -> TicketView:
        for t in self.get_all_tickets(user_id=user_id).list_tickets:
            if ticket_id==t.ticket_id:
                return t
        return TicketView(ticket_id=0,describe="",statuses=[])
