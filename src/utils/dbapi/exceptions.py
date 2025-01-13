class DBException(Exception):
    base_message = f''

    def __init__(self, message=''):
        self.m = message
        self.create_message()
        super().__init__(self.base_message)

    def create_message(self):
        self.base_message = self.base_message + f'{self.m}'

class DBConnectError(DBException):
    base_message = f"The connection isn't established "

class DBOperationError(DBException):
    base_message=f"The operation error is: "
