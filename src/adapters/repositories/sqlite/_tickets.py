import datetime


from src.adapters.repository import AbstractRepositoryTicket, _RepositoryStatus
from src.domain.ticket import Ticket
from src.utils.dbapi.connect import Connection


class SQLiteRepositoryTicket(AbstractRepositoryTicket):
    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.select_id=self.conn.create_query("select t.ticket_id, t.describes, ts.status_ticket_id,ts.date_, "
                                              "ts.comment FROM tickets t LEFT JOIN ticket_status ts ON t.ticket_id = "
                                              "ts.ticket_id WHERE t.user_id = :user_id ORDER BY t.ticket_id, ts.date_",
                                              var=["id","describe","status_ticket","date","comment"])

        self.insert=self.conn.create_query("INSERT INTO tickets (user_id,describes) VALUES (:user_id,:describes)")
        self.update=self.conn.create_query("UPDATE tickets SET user_id=:user_id, describes=:describe WHERE ticket_id=:ticket_id")


    def _get(self, user_id: int):
        tickets: [Ticket] = []
        records=self.select_id.get_result(params={"user_id":user_id})

        ticket_id = 0
        for r in records:
            ts = _RepositoryStatus.get_status_by_id(r["status_ticket"])
            s = ts(date=datetime.datetime.fromisoformat(r["date"]),comment=r["comment"])
            if r["id"] != ticket_id:
                t = Ticket(ticket_id=r["id"], describe=r["describe"], statuses=[s])
                tickets.append(t)
                ticket_id = r["id"]
                continue
            tickets[-1].statuses.append(s)
        return tickets

    def _save(self, user_id: int, ticket: Ticket) -> Ticket:
        if not ticket.ticket_id:
            ticket.ticket_id=self.insert.set_result(params={"user_id":user_id,"describes":ticket.describe})
        else:
            ticket.ticket_id=self.update.set_result(params={"user_id":user_id,'describe':ticket.describe,'ticket_id':ticket.ticket_id})
            if ticket.ticket_id==0:
                return ticket
            count=self.conn.create_query("SELECT count(status_ticket_id) FROM ticket_status WHERE ticket_id=:ticket_id",
                                                params={'ticket_id': ticket.ticket_id}).get_one_result()


            insert_status=self.conn.create_query("INSERT INTO ticket_status (ticket_id,status_ticket_id,date_,comment) "
                           "VALUES(:ticket_id,:status_ticket_id,:date,:comment)")
            for t in ticket.statuses[count:]:
                insert_status.set_result(params=
                           {'ticket_id': ticket.ticket_id,
                            'status_ticket_id': _RepositoryStatus.get_id_by_status(t),
                            'date': t.date.isoformat(),
                            'comment': t.comment})
            return ticket

    def _delete(self, user_id: int, ticket_id: int) -> bool:
        delete_status=self.conn.create_query("DELETE FROM ticket_status WHERE ticket_id=:ticket_id",params={'ticket_id': ticket_id})
        delete_status.set_result()

        delete_ticket=self.conn.create_query("DELETE FROM tickets WHERE user_id=:user_id AND ticket_id=:ticket_id",
                            params={'user_id': user_id, 'ticket_id': ticket_id})
        delete_ticket.set_result()
        return bool(delete_ticket.count)
