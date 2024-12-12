from dataclasses import dataclass


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
