

from src.domain.status import ClientStatusDisabled, ClientStatusOperation
from src.utils.dbapi.connect import Connection
from src.viewers.clients import AbstractClientViewer
from src.viewers.data import ClientView


class SQLiteClientViewer(AbstractClientViewer):


    def __init__(self, conn:Connection):
        super().__init__()
        self.conn = conn

    def get_client(self, client_id: int) -> ClientView:
        query=self.conn.create_query("SELECT client_id, name,code1s,is_active FROM clients WHERE client_id=:client_id",
                                     var=["id","name","code1s","status"],
                                     params={'client_id': client_id})
        r=query.get_one_result()

        if len(r)==0:
            return ClientView(id=0, name="",code1s="",status=ClientStatusOperation.by_id(0))
        else:
            tc = ClientView(id=r["id"], name=r["name"], code1s=r["code1s"],status=ClientStatusOperation.by_id(r["status"]))
        return tc


    def get_client_by_name(self, name:str) -> list[ClientView]:
        list_view=[]
        query=self.conn.create_query("SELECT client_id, name,code1s,status FROM clients WHERE name=:name",
                                     var=["id","name","code1s","status"],
                       params={'name': name})
        r=query.get_result()
        if len(r) == 0:
            return []
        for i in r:
            list_view.append(ClientView(id=i["id"], name=i["name"], code1s=i["code1s"],status=ClientStatusOperation.by_id(i["status"])))
        return list_view




    def get_all_clients(self)->list[ClientView]:
        list_view = []
        query = self.conn.create_query("SELECT client_id, name,code1s,is_active FROM clients",
                                       var=["id", "name", "code1s", "status"])
        r = query.get_result()
        if len(r) == 0:
            return []
        for i in r:
            list_view.append(ClientView(id=i["id"], name=i["name"], code1s=i["code1s"],
                                        status=ClientStatusOperation.by_id(i["status"])))
        return list_view

