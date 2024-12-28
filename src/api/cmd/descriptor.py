import json

class ArgumentWrong(Exception):
    base_message = f'The argument is wrong'

    def __init__(self, message=''):
        if message:
            self.base_message=message
        super().__init__(self.base_message)


class InputLine:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        instance.arg = ""


class InputLineInt(InputLine):
    def __set__(self, instance, value):
        try:
            instance.__dict__[self.name] = value
            if not value:
                instance.arg = 0
            else:
                instance.arg = int(value)
        except ValueError:
            raise ArgumentWrong

class InputLineStr(InputLine):
    def __set__(self, instance, value):
        try:
            instance.__dict__[self.name] = value
            if not value:
                instance.arg = ''
            else:
                instance.arg = str(value)
        except ValueError:
            raise ArgumentWrong



class InputLineJSON(InputLine):
    def __set__(self, instance, value):
        try:
            instance.arg = json.loads(value)
            instance.__dict__[self.name] = value
        except json.decoder.JSONDecodeError:
            raise ArgumentWrong


class Command:
    input_line: str = InputLine()
    arg: str
    addition: dict = {}

    def __init__(self, input_line: str):
        self.input_line = input_line


class CommandStr:
    input_line = InputLineInt()
    arg:str

class CommandInt(Command):
    input_line = InputLineInt()
    arg: int


class CommandJSON(Command):
    input_line = InputLineJSON()
    arg: json
