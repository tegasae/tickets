from dataclasses import dataclass

@dataclass
class Command:
    command="empty"

@dataclass
class Create(Command):
    command='Create'
    user_id: int
    describe: str
    comment: str

@dataclass
class Cancel(Command):
    command='Cancel'
    ticket_id: int
    user_id: int
    command:str