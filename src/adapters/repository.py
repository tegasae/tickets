import abc

from src.domain.ticket import User, Ticket


class AbstractRepositoryUser(abc.ABC):
    def __init__(self):
        self.seen_users: dict[int, User] = {}

    def save(self, user: User):
        user = self._save(user=user)
        if user.user_id:
            self.seen_users[user.user_id] = user

    def get(self, user_id: int) -> User:
        user = self._get(user_id=user_id)
        if user.user_id:
            self.seen_users[user_id] = user
        return user

    @abc.abstractmethod
    def _save(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_id: int) -> User:
        raise NotImplementedError


class AbstractRepositoryTicket(abc.ABC):
    def __init__(self):
        self.seen_ticketes: dict[int, Ticket] = {}

    @abc.abstractmethod
    def save(self, ticket: Ticket):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ticket_id: Ticket) -> Ticket:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, user_id: int) -> list[Ticket]:
        raise NotImplementedError
