import sqlite3
from sqlite3 import OperationalError

from src.adapters.repository import AbstractRepositoryUser
from src.domain.exceptions import TicketNotFound
from src.domain.status import UserStatusDisabled, UserStatusEnabled, ClientStatusDisabled, ClientStatusEnabled
from src.domain.ticket import User, Client
from src.utils.dbapi.connect import Connection
from src.utils.dbapi.exceptions import DBOperationError
from src.utils.dbapi.query import Query

UserStatusId = {
    UserStatusDisabled: 0,
    UserStatusEnabled: 1
}

ClientStatusId = {
    ClientStatusDisabled: 0,
    ClientStatusEnabled: 1
}


def get_user_status_by_id(status_id: int):
    for i in UserStatusId.keys():
        if UserStatusId[i] == status_id:
            return i
    return UserStatusDisabled


def get_client_status_by_id(status_id: int):
    for i in ClientStatusId.keys():
        if ClientStatusId[i] == status_id:
            return i
    return ClientStatusDisabled


class SQLiteRepositoryUser(AbstractRepositoryUser):
    insert_user: Query

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.insert_user=self.conn.create_query("INSERT INTO users (client_id,name,is_active) VALUES (:client_id,:name,:is_active)")
        self.update_user=self.conn.create_query("UPDATE users SET client_id=:client_id, name=:name, is_active=:is_active WHERE user_id=:user_id")
        self.get_user=self.conn.create_query("SELECT u.user_id, u.name, u.is_active,c.client_id,c.name,c.is_active "
                                             "FROM users u "
                                             "LEFT JOIN clients c ON u.client_id=c.client_id WHERE u.user_id=:user_id",
                                             var=["id","name","status","client_id","client_name","client_status"])
        self.delete_user=self.conn.create_query("DELETE FROM users WHERE user_id=:user_id")

    def _save(self, user: User) -> User:
        try:
            if not user.user_id:
                user.user_id=self.insert_user.set_result(params={'client_id': user.client.client_id, 'name': user.name, 'is_active': user.is_active()})
            else:
                last_id=self.update_user.set(param={'client_id': user.client.client_id, 'name': user.name, 'is_active': user.is_active(), 'user_id': user.user_id})
                if last_id==0:
                    user.user_id=0
        except DBOperationError:
            user.user_id=0

        return user

    def _get(self, user_id: int) -> User:
        r=self.get_user.get_one_result(params={'user_id': user_id})

        if len(r) is None:
            return User(user_id=0, name="", client=Client(client_id=0, name="", status=ClientStatusDisabled()),
                        status=UserStatusDisabled())
        client_status = get_client_status_by_id(r["client_status"])
        client = Client(client_id=r["client_id"], name=r["client_name"], status=client_status())
        status = get_user_status_by_id(r["status"])

        user = User(user_id=r["id"], name=r["name"], client=client, tickets=[], status=status())

        return user

    def _delete(self, user_id: int) -> bool:
        self.delete_user.set_result(params={'user_id': user_id})

        if self.delete_user.count > 0:
            return True
        else:
            return False
