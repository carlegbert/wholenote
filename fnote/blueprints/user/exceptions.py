class UserExistsError(Exception):
    """
    Exception raised when trying to insert duplicate
    users into the database
    Attributes:
        email -- email of user attempted to insert into db
        message -- explanation of the error
    """
    def __init__(self, email):
        self.email = email
        self.message = email + ' already exists in user database'


class UserNotFoundError(Exception):
    """Exception raised when user not found in database
    Attributes:
        email -- email that was not found
        message -- explanation of the error
    """
    def __init__(self, email):
        self.email = email
        self.message = email + 'not found'


class WrongPasswordError(Exception):
    """Exception raised when incorrect password is attempted
    Attributes:
        email -- email of user
        message -- explanation of the error
    """
    def __init__(self, email):
        self.email = email
        self.message = 'Incorrect password for ' + email
