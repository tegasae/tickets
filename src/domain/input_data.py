from dataclasses import dataclass

from src.domain.status import ClientStatus


@dataclass(frozen=True)
class DataForTicket:
    user_id: int
    describe: str
    comment: str

@dataclass
class DataCancelTicket:
    user_id: int
    ticket_id: int
    comment: str

@dataclass
class DataClient:
    client_id:int
    name: str
    enable: bool


