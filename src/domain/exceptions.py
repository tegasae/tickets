class CommonException(Exception):
    base_message = f''

    def __init__(self, message=''):
        self.m = message
        self.create_message()
        super().__init__(self.base_message)

    def create_message(self):
        self.base_message = f'{self.m}'


class UserNotFound(CommonException):
    def create_message(self):
        self.base_message = f'The user isn\'t found{self.m}'


class TicketNotFound(CommonException):
    def create_message(self):
        self.base_message = f'The ticket isn\'t found {self.m}'
