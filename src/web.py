import sqlite3
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from src.domain.input_data import DataClient
from src.services.service_layer.client import get_client, list_clients, save_client
from src.services.service_layer.ticket import get_all_tickets, get_ticket
from src.services.uow.sqlite.unit_of_work import SQLLiteUnitOfWork

dependency = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect('data/tickets.db')
    uow: SQLLiteUnitOfWork = SQLLiteUnitOfWork(connection=conn)

    dependency['uow'] = uow
    yield dependency

    conn.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ticket/{user_id}")
async def read_tickets(user_id: int, ticket_id: int = 0):
    if ticket_id == 0:
        return get_all_tickets(user_id=user_id, uow=dependency['uow']).list_tickets
    else:
        return get_ticket(user_id=user_id, ticket_id=ticket_id, uow=dependency['uow'])


@app.get("/clients")
async def read_clients():
    clients = list_clients(uow=dependency['uow'])
    if len(clients) == 0:
        raise HTTPException(status_code=404, detail="Clients not found")
    return clients


# def save(argument:CommandJSON)->int:
#    try:
#        dc=DataClient(client_id=argument.arg['id'],name=argument.arg['name'],enable=argument.arg['enable'])
#        client=save_client(dc=dc,uow=argument.addition['uow'])
#        if client.client_id==0:
#            return "The operations didn't execute"
#        return client.client_id
#    except ValueError:
#        return "The data is wrong"
class dcBm(BaseModel):
    name:str
    enable: bool=True

@app.post("/client/",status_code=201)
async def create(client_bm: dcBm):

    dc=DataClient(client_id=0,name=client_bm.name,enable="true")
    client = save_client(dc=dc, uow=dependency["uow"])
    if client.client_id==0:
        raise HTTPException(status_code=409,detail="Cannot create")
    return client.client_id


# @command_wrapper(name="change_client", descriptor=CommandJSON)
# def change(argument:CommandJSON)->str:
#    return save(argument)

# @command_wrapper(name="delete_client",descriptor=CommandInt)
# def delete(argument:CommandInt):
#    if argument.arg:
#        r=delete_client(client_id=argument.arg,uow=argument.addition['uow'])
#        if r:
#            return "Delete"
#        else:
#            return "didn't delete"


# @app.get("/ticket/{ticket_id}")
# def read_item(ticket_id: int, q: Union[str, None] = None):
#    return {"ticket_id": ticket_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
