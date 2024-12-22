from src.api.cmd.cmd import command_wrapper
from src.api.cmd.descriptor import CommandInt, CommandJSON, Command
from src.domain.input_data import DataCancelTicket, DataForTicket
from src.services.service_layer import get_ticket, cancel_ticket, create_ticket


@command_wrapper(name="get_user",descriptor=CommandInt)
def get_all(argument:CommandInt):
    print(get_ticket(user_id=argument.user.user_id, ticket_id=argument.arg, uow=argument.uow))

