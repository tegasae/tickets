import sqlite3

from src.adapters.repository import AbstractRepositoryUser
from src.domain.status import UserStatusDisabled, UserStatusEnabled
from src.domain.ticket import User, Client

UserStatusId = {
    UserStatusDisabled: 0,
    UserStatusEnabled: 1
}


class SQLiteRepositoryUser(AbstractRepositoryUser):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.connect = conn

    #def _get_tickets(self, user_id: int) -> [Ticket]:


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


        user = User(user_id=r[0], name=r[1], client=client, tickets=[], status=r[2])
        return user

    def _delete(self, user_id: int) -> bool:
        cursor = self.connect.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=:user_id", {'user_id': user_id})
        if cursor.rowcount > 0:
            return True
        else:
            return False
