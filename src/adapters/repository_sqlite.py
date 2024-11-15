import datetime
import sqlite3

from src.adapters.repository import AbstractRepositoryUser
from src.domain.status import TicketStatus, TicketStatusExecuted, TicketStatusAccepted, TicketStatusConfirmed, \
    TicketStatusCancelledUser, TicketStatusCancelledOperator, ClientStatusEnabled, UserStatusEnabled, UserStatusDisabled
from src.domain.ticket import Client, User, Ticket

TicketStatusId = {
    1: TicketStatus,
    2: TicketStatusAccepted,
    3: TicketStatusConfirmed,
    4: TicketStatusExecuted,
    5: TicketStatusCancelledUser,
    6: TicketStatusCancelledOperator
}

UserStatusId = {
    UserStatusDisabled: 0,
    UserStatusEnabled: 1
}


class SQLiteRepositoryUser(AbstractRepositoryUser):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.connect = conn

    def _get_tickets(self, user_id: int) -> [Ticket]:
        tickets: [Ticket] = []
        select_tickets = (
            "select t.ticket_id, t.describes, st.status_ticket_id, st.status_ticket,ts.date_, ts.comment  "
            "FROM tickets "
            "t LEFT JOIN ticket_status ts ON t.ticket_id = ts.ticket_id LEFT JOIN statuses_ticket st ON "
            "ts.status_ticket_id = st.status_ticket_id  WHERE t.user_id =:user_id ORDER BY t.ticket_id, "
            "ts.date_")
        cursor = self.connect.cursor()
        cursor.execute(select_tickets, {'user_id': user_id})
        records = cursor.fetchall()
        ticket_id = 0

        for r in records:
            ts = TicketStatusId[r[2]](date=datetime.datetime.fromisoformat(r[4]), comment=r[5])
            if r[0] != ticket_id:
                t = Ticket(ticket_id=r[0], describe=r[1], statuses=[ts])
                tickets.append(t)
                ticket_id = r[0]
                continue
            tickets[-1].statuses.append(ts)

        return tickets

    def _save(self, user: User) -> User:
        cursor = self.connect.cursor()

        if not user.user_id:
            cursor.execute("INSERT INTO users (client_id,name,is_active) VALUES (:client_id,:name,:is_active)",
                           {'client_id': user.client.client_id, 'name': user.name, 'is_active': user.is_active()})
            user.user_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE users SET client_id=:client_id, name=:name, is_active=:is_active "
                           "WHERE user_id=:user_id",
                           {'client_id': user.client.client_id, 'name': user.name, 'is_active': user.is_active(),
                            'user_id': user.user_id})
        return user

    def _get(self, user_id: int) -> User:
        cursor = self.connect.cursor()
        cursor.execute("SELECT u.user_id, u.name, u.is_active,c.client_id,c.name,c.is_active FROM users u "
                       "LEFT JOIN clients c ON u.client_id=c.client_id "
                       "WHERE u.user_id=:user_id",
                       {'user_id': user_id})
        r = cursor.fetchone()
        client = Client(client_id=r[3], name=r[4], status=r[5])
        tickets = self._get_tickets(user_id=r[0])
        user = User(user_id=r[0], name=r[1], client=client, tickets=tickets, status=r[2])
        return user

    def _delete(self, user_id: int) -> bool:
        cursor = self.connect.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=:user_id AND (SELECT count(ticket_id) FROM tickets WHERE "
                       "user_id=:user_id)=0",
                       {'user_id': user_id})
        if cursor.rowcount > 0:
            return True
        else:
            return False


if __name__ == "__main__":
    tick: [Ticket]
    connect = sqlite3.connect(database="../../data/tickets.db")
    s = SQLiteRepositoryUser(conn=connect)
    user = User(user_id=0, name="user1", client=Client(client_id=1,name="client",status=ClientStatusEnabled()), status=UserStatusDisabled())
    s.save(user=user)
    connect.commit()

    cur = connect.cursor()
    cur.execute("SELECT user_id,client_id,name,is_active FROM users WHERE user_id=4")
    r = cur.fetchone()
    print(type(user.status))
    print(r)
    connect.commit()
    connect.close()
