from dataclasses import dataclass
from typing import Callable




@dataclass
class Cmd:
    command: str
    arg: str = ""


HANDLERS:dict[str,Callable]={}


def command(name: str):
    def inner_decorator(f):
        HANDLERS[name] = f

        def wrapper(*args, **kwargs):
            print(name)
            f(*args, **kwargs)
            print("2")

        return wrapper

    return inner_decorator


def parse_cmd(cmd_str: str) -> Cmd:
    index = cmd_str.rstrip().find(" ")
    if index != -1:  # Check if a space exists
        c = Cmd(command=cmd_str[:index].lower(), arg=cmd_str[index + 1:])
    else:
        c = Cmd(command=cmd_str.lower())
    return c


def cmd_process():
    while True:
        cmd = parse_cmd(cmd_str=input(">"))
        f = HANDLERS.get(cmd.command, None)
        if f is None:
            continue
        f(cmd.arg)
