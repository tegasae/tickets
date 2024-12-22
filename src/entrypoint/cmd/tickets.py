from src.api.cmd.cmd import parse_cmd, HANDLERS, DESCRIPTOR, command_wrapper
from src.api.cmd.descriptor import Command
from src.services.service_layer import get_all_tickets


def cmd_process(**kwargs):
    while True:
        (command_str,raw_arg) = parse_cmd(cmd_str=input(">"))

        f = HANDLERS.get(command_str, None)
        arg=DESCRIPTOR.get(command_str,None)

        if f is None or arg is None:
            continue
        c = arg(input_line=raw_arg)
        for k in kwargs:
            setattr(c, k, kwargs[k])
        f(c)


@command_wrapper(name="list",descriptor=Command)
def get_all(argument:Command):
    print(get_all_tickets(user_id=argument.user.user_id, uow=argument.uow))
