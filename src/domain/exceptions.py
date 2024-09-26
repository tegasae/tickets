class CommonException(Exception):
    base_message = f''

    def __init__(self, message=''):
        self.m = message
        self.create_message()
        super().__init__(self.base_message)

    def create_message(self):
        self.base_message = f'{self.m}'


class InvalidStatus(CommonException):
    def create_message(self):
        self.base_message = f'The status isn''t correct {self.m}'
