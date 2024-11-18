import datetime

from src.domain.exceptions import InvalidStatus
from src.domain.status import TicketStatus, TicketStatusAccepted, TicketStatusConfirmed, TicketStatusExecuted, \
    TicketStatusCancelledUser, TicketStatusCancelledOperator


class _StoreStatus:
    TicketStatusId = {
        1: TicketStatus,
        2: TicketStatusAccepted,
        3: TicketStatusConfirmed,
        4: TicketStatusExecuted,
        5: TicketStatusCancelledUser,
        6: TicketStatusCancelledOperator
    }
    @staticmethod
    def get_status(ticket_status):
        for t in _StoreStatus.TicketStatusId:
            if type(ticket_status) is _StoreStatus.TicketStatusId[t]:
                return t
        return _StoreStatus.TicketStatusId[1]

    @staticmethod
    def store_status(cursor,ticket_id,statuses):
        for status in statuses:
            cursor.execute("INSERT INTO ticket_status (ticket_id,status_ticket_id,date_,comment)"
                           " VALUES (:ticket_id,:status_ticket_id,:date,:comment)",
                           {'ticket_id': ticket_id, 'status_ticket_id': _StoreStatus.get_status(status),
                            'date': status.date.isoformat(), 'comment': status.comment})

    @staticmethod
    def count_statues(cursor,ticket_id)->int:
        cursor.execute("SELECT count(ticket_id) FROM ticket_status WHERE ticket_id=:ticket_id",{'ticket_id':ticket_id})
        return cursor.fetchone()[0]

    @staticmethod
    def delete_statues(cursor,ticket_id):
        cursor.execute("DELETE FROM ticket_status WHERE ticket_id=:ticket_id",{'ticket_id':ticket_id})

    @staticmethod
    def create_status(status_id:int,date:str,comment:str):
        #try:
        print("!!!!")
        print(status_id)
        ts=_StoreStatus.TicketStatusId[status_id](date=datetime.datetime.fromisoformat(date), comment=comment)
        #except KeyError:
            #ts = _StoreStatus.TicketStatusId[1](date=datetime.datetime.fromisoformat(date), comment=comment)
        return ts

