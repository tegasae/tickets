import json
from typing import Union

from src.domain.status import TicketStatus, TicketStatusAccepted
from src.domain.ticket import Ticket



def ticket_to_dict(ticket:Ticket) -> dict:
    d={'id':ticket.ticket_id, 'describe':ticket.describe,'date_created':ticket.date_created.isoformat(),'statuses':[]}
    for s in ticket.statuses:
        ds={'status':s.name,'date':s.date.isoformat(),'comment':s.comment}
        d['statuses'].append(ds)
    return d

def ticket_to_json(ticket:Ticket)->json:
    return json.dumps(ticket_to_dict(ticket=ticket))

def list_tickets_to_json(tickets:list[Ticket])->json:
    tl=[]
    for t in tickets:
        tl.append(ticket_to_dict(ticket=t))
    return json.dumps(tl)
