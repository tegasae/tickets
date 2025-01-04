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
    def __post_init__(self):
        if type(self.client_id) is not int and self.client_id<0:
            raise ValueError
        self.name=self.name.lstrip()
        if not len(self.name):
            raise ValueError()
        if self.enable!='true' and self.enable!='false':
            raise ValueError
        if self.enable=='true':
            self.enable=True
        if self.enable=='false':
            self.enable=False

