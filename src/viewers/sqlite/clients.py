import logging

from src.domain.client import ClientStatusOperation
from src.utils.dbapi.connect import Connection
from src.viewers.clients import AbstractClientViewer
from src.viewers.data import ClientView

logger = logging.getLogger(__name__)

class SQLiteClientViewer(AbstractClientViewer):
    def __init__(self, conn:Connection):
        super().__init__()
        self.conn = conn

    def get_client(self, client_id: int) -> ClientView:
        logger.debug("123")
        query=self.conn.create_query("SELECT client_id, name,code1s,is_active FROM clients WHERE client_id=:client_id",
                                     var=["id","name","code1s","status"],
                                     params={'client_id': client_id})
        r=query.get_one_result()

        if len(r)==0:
            return ClientView(id=0, name="",code1s="",status=ClientStatusOperation.by_id(0))
        else:
            tc = ClientView(id=r["id"], name=r["name"], code1s=r["code1s"],status=ClientStatusOperation.by_id(r["status"]))
        return tc
    def _get_by_something(self,param:str,value:str,order:str="",direct:bool=True)->list[ClientView]:
        where=""
        if param!="":
            where=f"WHERE {param}=:{param} "

        if direct is True:
            direct="ASC"
        else:
            direct="DESC"
        sort=""
        if order!="":
            sort = f" ORDER BY {order} {direct}"



        sql=f"SELECT client_id, name,code1s,is_active FROM clients {where} {sort}"
        query=self.conn.create_query(sql=sql,var=["id","name","code1s","status"],params={param:value})
        list_view=[]
        for i in query.get_result():
            list_view.append(ClientView(id=i["id"], name=i["name"], code1s=i["code1s"],
                                        status=ClientStatusOperation.by_id(i["status"])))
        return list_view

    def get_client_by_name(self, name:str) -> list[ClientView]:
        return self._get_by_something(param="name",value=name,order="name",direct=True)


    def get_client_by_code1s(self, code1s:str) -> list[ClientView]:
        return self._get_by_something(param="code1s", value=code1s, order="name", direct=True)

    def get_all_clients(self)->list[ClientView]:
        return self._get_by_something(param="",value="")

