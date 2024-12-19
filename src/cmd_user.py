from src.api.cmd.cmd import command, cmd_process


@command(name="exit")
def exit_cmd(argument: str):
    exit()


@command(name="exit1")
def exit_new(argument: str):
    print(argument)
    print("exit_new")


if __name__ == '__main__':
    cmd_process()
