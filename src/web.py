import logging
import sqlite3
from typing import Union

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from src.domain import messages
from src.services import messagebus
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork
from src.utils.dbapi.connect import Connection
from src.viewers.sqlite.clients import SQLiteClientViewer


class ClientHTTP(BaseModel):
    client_id:int=0
    name:str
    code1s:str=""
    enable:bool


app = FastAPI()
conn = Connection.create_connection(url="../data/tickets.db", engine=sqlite3)
uow = SQLLiteUnitOfWork(connection=conn)
client_viewer = SQLiteClientViewer(conn=conn)

logging.basicConfig(format='%(asctime)s %(filename)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)




@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/clients/")
async def read_clients():
    logger.debug("read clients")
    return client_viewer.get_all_clients()


@app.get("/clients/{client_id}")
async def read_client(client_id: int, q: Union[str, None] = None):
    return client_viewer.get_client(client_id=client_id)


@app.get('/clients/by-name/{client_name}')
async def read_client_name(client_name: str):
    return client_viewer.get_client_by_name(name=client_name)


@app.get('/clients/by-code/{code}')
async def read_client_name(code1s: str):
    return client_viewer.get_client_by_code1s(code1s=code1s)


@app.post('/clients/')
async def create_client(client_http:ClientHTTP):
    cmd=messages.CreateClient(name=client_http.name,code1s=client_http.code1s,enable=client_http.enable)
    messagebus.handle(cmd,uow)
    return client_http


if __name__ == "__main__":
    uvicorn.run("web:app", host="127.0.0.1", port=8000, reload=True)
