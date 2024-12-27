from typing import Callable

from src.api.cmd.descriptor import Command, ArgumentWrong

HANDLERS: dict[str, Callable] = {}
DESCRIPTOR: dict[str, Callable] = {}


def command_wrapper(name: str, descriptor: type(Command)):
    def inner_decorator(f):
        HANDLERS[name] = f
        DESCRIPTOR[name] = descriptor

        def wrapper(*args, **kwargs):
            print(name)
            f(*args, **kwargs)
            print("2")

        return wrapper

    return inner_decorator


def parse_cmd(cmd_str: str):
    index = cmd_str.rstrip().find(" ")
    if index != -1:  # Check if a space exists
        return cmd_str[:index].lower(), cmd_str[index + 1:]
    else:
        return cmd_str.lower(), ""


def cmd_process(**kwargs):
    while True:

        try:
            (command_str, raw_arg) = parse_cmd(cmd_str=input(">"))

            f = HANDLERS[command_str]
            arg = DESCRIPTOR.get(command_str, None)


            c = arg(input_line=raw_arg)
            for k in kwargs:
                c.addition[k] = kwargs[k]
            s=f(c)
            print(s)
        except KeyError:
            print("The command is wrong")
        except ArgumentWrong:
            print("The argument is wrong")

