from werkzeug.security import generate_password_hash, check_password_hash

from fnote.blueprints.user.exceptions import UserExistsError
from fnote.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        self.email = kwargs.get('email', '')
        self.password = User.encrypt_pw(kwargs.get('password', ''))

    @classmethod
    def register(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        if User.find_by_identity(email):
            raise UserExistsError(email)
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def find_by_identity(cls, email):
        """
        :param email:
        :type email: str
        :return: User
        """
        return User.query.filter(User.email == email).first()

    @classmethod
    def encrypt_pw(cls, pw_plain):
        """
        Encrypt with PBKDF2
        :param pw_plain: Plaintext password
        :type pw_plain: str
        :return: str
        """
        return generate_password_hash(pw_plain)

    def check_password(self, pw_plain):
        """
        Check plaintext password against database
        :param pw_plain: Plaintext password
        :type pw_plain: str
        :return: bool
        """
        return check_password_hash(self.password, pw_plain)

    def update_email(self, new_email):
        """
        Update user's email in database. Throws UserExistsError if new email
        already exists in database. Other validation should be happen in
        views.py
        :param new_email: New email
        :type new_email: str
        :return: updated User object
        """
        if (User.find_by_identity(new_email)):
            raise UserExistsError(new_email)
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return self

    def update_password(self, new_password):
        """
        Update user's password in database.
        :param new_password: New password
        :type new_password: str
        :return: updated User object
        """
        self.password = User.encrypt_pw(new_password)
        db.session.add(self)
        db.session.commit()
        return self
