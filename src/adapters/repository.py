import abc
from abc import abstractmethod

from src.domain.exceptions import UserNotFound
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

    def delete(self,user_id:int):
        if not self._delete(user_id):
            raise UserNotFound()
        if user_id in self.seen_users:
            del(self.seen_users[user_id])


    @abc.abstractmethod
    def _save(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, user_id: int) -> bool:
        raise NotImplementedError



class AbstractRepositoryTicket(abc.ABC):
    def __init__(self):
        self.seen_user_tickets: dict[int, list[Ticket]] = {}

    def save(self,user_id:int,ticket:Ticket)->Ticket:
        ticket=self._save(user_id,ticket)
        try:
            index=self.seen_user_tickets[user_id].index(ticket)
            self.seen_user_tickets[user_id][index]=ticket
        except KeyError:
            self.seen_user_tickets[user_id]=[]
            self.seen_user_tickets[user_id].append(ticket)
        except  ValueError:
            self.seen_user_tickets[user_id].append(ticket)

        return ticket

    def get(self,user_id:int)->list[Ticket]:
        return self._get(user_id)



    def delete(self,user_id:int,ticket_id:int):
        if self._delete(user_id,ticket_id) and user_id in self.seen_user_tickets:
            del(self.seen_user_tickets[user_id])
        else:
            raise

    @abc.abstractmethod
    def _save(self, user_id: int, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_id: int) -> list[Ticket]:
        raise NotImplementedError


    @abc.abstractmethod
    def _delete(self, user_id: int, ticket_id: int)->bool:
        raise NotImplemented