from dataclasses import dataclass, asdict, field


@dataclass
class StatusView:
    id:int
    date:str
    name:str
    comment:str=""

@dataclass(kw_only=True)
class TicketView:
    ticket_id:int
    describe:str
    statuses:list[StatusView]
    active_status:StatusView= field(init=False)
    def __post_init__(self):
        self.active_status=self.statuses[-1]

    def __repr__(self):
        return repr(asdict(self))

@dataclass(kw_only=True)
class ListTicketView:
    list_tickets:[TicketView]=field(default_factory=list)
    def __repr__(self):
        d=asdict(self)
        return repr(d['list_tickets'])

