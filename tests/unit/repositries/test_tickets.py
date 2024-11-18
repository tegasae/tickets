from src.adapters.repositories.sqlite import SQLiteRepositoryTicket
from src.domain.status import TicketStatusAccepted, TicketStatusConfirmed
from src.domain.ticket import Ticket


def test_save_ticket(create_conn):
    tr = SQLiteRepositoryTicket(conn=create_conn)
    ticket=Ticket(statuses=[TicketStatusAccepted(),TicketStatusConfirmed()])
