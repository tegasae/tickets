from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserStatus:
    name: str="User Status"


@dataclass
class UserStatusEnabled(UserStatus):
    name: str="Enable"

@dataclass
class UserStatusDisabled(UserStatus):
    name="Disable"


@dataclass
class TicketStatus:
    name="Status"

@dataclass
class TicketStatusAccepted(TicketStatus):
    name="Accept from an user"


@dataclass
class TicketStatusConfirmed(TicketStatus):
    name="Confirmed by an operator"

@dataclass
class TicketStatusExecuted(TicketStatus):
    name="Executed"


@dataclass
class TicketStatusCancelledUser(TicketStatus):
    name="Cancelled by an user"


@dataclass
class TicketStatusCancelledOperator(TicketStatus):
    name="Cancelled by an operator"




