import sqlite3

from src.domain.status import ClientStatusDisabled, ClientStatusOperation
from src.viewers.clients import AbstractClientViewer
from src.viewers.data import ClientView


class SQLiteClientViewer(AbstractClientViewer):


    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn

    def get_client(self, client_id: int) -> ClientView:
        cursor = self.conn.cursor()

        cursor.execute("SELECT client_id, name,code1s,is_active FROM clients WHERE client_id=:client_id",
                       {'client_id': client_id})
        r = cursor.fetchone()
        if r is None:
            return ClientView(id=0, name="",code1s="",status=ClientStatusOperation.by_id(0))
        else:
            tc = ClientView(id=r[0], name=r[1], code1s=r[2],status=ClientStatusOperation.by_id(r[3]))
        return tc


    def get_client_by_name(self, name:str) -> list[ClientView]:
        cursor = self.conn.cursor()
        list_view=[]
        cursor.execute("SELECT client_id, name,code1s,status FROM clients WHERE name=:name",
                       {'name': name})
        r = cursor.fetchall()
        if len(r) == 0:
            return []
        for i in r:
            list_view.append(ClientView(id=i[0], name=i[1], code1s=i[2],status=ClientStatusOperation.by_id(i[3])))
        return list_view




    def get_all_clients(self)->list[ClientView]:
        cursor = self.conn.cursor()
        list_view = []
        cursor.execute("SELECT client_id, name,code1s,is_active FROM clients")
        r = cursor.fetchall()
        if len(r) == 0:
            return []
        for i in r:
            status=ClientStatusOperation.by_id(i[3])
            list_view.append(ClientView(id=i[0], name=i[1], code1s=i[2], status=status))
        return list_view

