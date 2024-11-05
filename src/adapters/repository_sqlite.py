from src.adapters.repository import AbstractRepository
from src.domain.ticket import Client


class SQLiteRepository(AbstractRepository):
    def __init__(self,connect):
        self.connect=connect

    def save(self, client: Client):
        cur = self.connect.cursor()


    def get(self, client_id) -> Client:
        cur = self.connect.cursor()

