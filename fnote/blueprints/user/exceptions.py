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
