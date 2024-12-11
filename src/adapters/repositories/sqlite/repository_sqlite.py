import sqlite3
from datetime import datetime

from src.adapters.repositories.sqlite import SQLiteRepositoryTicket

from src.domain.ticket import Client, User, Ticket

if __name__ == "__main__":
    tick: [Ticket]
    connect = sqlite3.connect(database="../../../../data/tickets.db")
    tr = SQLiteRepositoryTicket(conn=connect)
    cur = connect.cursor()
    cur.execute("DELETE FROM tickets")
    cur.execute("DELETE FROM ticket_status")
    cur.execute("INSERT INTO tickets (ticket_id,user_id,describes) VALUES(1,1,'123')")
    cur.execute("INSERT INTO ticket_status (ticket_id,status_ticket_id,date_,comment) VALUES(1,2,'2024-11-19T00:19:42.816100','123')")
    cur.execute("INSERT INTO ticket_status (ticket_id,status_ticket_id,date_,comment) VALUES(1,3,'2024-11-19T00:19:42.816100','123')")

    # ticket1 = Ticket(describe="456")
    # tr.save(user_id=1, ticket=ticket1)
    tickets = tr.get(user_id=1)
    print(tickets)
    connect.commit()
