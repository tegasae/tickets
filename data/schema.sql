CREATE TABLE IF NOT EXISTS "statuses_ticket" (
	status_ticket_id INTEGER NOT NULL,
	status_ticket TEXT,
	CONSTRAINT statuses_ticket_pk PRIMARY KEY (status_ticket_id)
);
CREATE TABLE clients (
	client_id INTEGER NOT NULL,
	name TEXT,
	is_active INTEGER DEFAULT (0), code1s TEXT,
	CONSTRAINT clients_pk PRIMARY KEY (client_id)
);
CREATE TABLE users (
	user_id INTEGER NOT NULL,
	client_id INTEGER,
	name TEXT, is_active INTEGER DEFAULT (0),
	CONSTRAINT users_pk PRIMARY KEY (user_id),
	CONSTRAINT users_clients_FK FOREIGN KEY (client_id) REFERENCES clients(client_id)
);
CREATE TABLE ticket_status (
	ticket_id INTEGER,
	status_ticket_id INTEGER,
	date_ TEXT, comment TEXT,
	CONSTRAINT ticket_status_statuses_ticket_FK FOREIGN KEY (status_ticket_id) REFERENCES "statuses_ticket"(status_ticket_id),
	CONSTRAINT ticket_status_tickets_FK FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);
CREATE TABLE tickets (
	ticket_id INTEGER NOT NULL,
	"describes" TEXT,
	code1s TEXT,
	user_id INTEGER,
	CONSTRAINT tickets_pk PRIMARY KEY (ticket_id),
	CONSTRAINT tickets_users_FK FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);
