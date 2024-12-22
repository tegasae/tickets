import json


class InputLine:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name]=value
        instance.arg = ""

class InputLineInt(InputLine):
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        instance.arg=int(value)



class InputLineJSON(InputLine):
    def __set__(self, instance, value):
        instance.arg=json.loads(value)
        instance.__dict__[self.name]=value



class Command:
    input_line:str=InputLine()
    arg:str
    def __init__(self,input_line:str):
        self.input_line=input_line

class CommandInt(Command):
    input_line = InputLineInt()
    arg:int

class CommandJSON(Command):
    input_line =InputLineJSON()
    arg:json

