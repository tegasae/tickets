from src.api.cmd.cmd import command_wrapper
from src.entrypoint.cmd.tickets import cmd_process
from src.api.cmd.descriptor import Command, CommandInt, CommandJSON


@command_wrapper(name="exit",descriptor=Command)
def exit_cmd(argument:Command):
    exit()


@command_wrapper(name="exit1",descriptor=Command)
def exit_new(argument:Command):
    print(argument.input_line)
    print(argument)
    print(type(argument))

@command_wrapper(name="get",descriptor=CommandInt)
def get(argument:Command):
    print(argument.input_line)
    print(argument)
    print(type(argument))

@command_wrapper(name="get_json",descriptor=CommandJSON)
def get_json(argument:Command):
    print(argument.input_line)
    print(argument)
    print(type(argument))




if __name__ == '__main__':
    cmd_process()
