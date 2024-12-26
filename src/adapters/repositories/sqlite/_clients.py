from src.adapters.repository import AbstractRepositoryClient
from src.domain.ticket import Client


class SQLiteRepositoryClient(AbstractRepositoryClient):
    def _save(self, client: Client) -> Client:
        print("save")

    def _get(self, client_id: int) -> Client:
        print("get")

    def _delete(self, client_id: int) -> bool:
        print("delete")