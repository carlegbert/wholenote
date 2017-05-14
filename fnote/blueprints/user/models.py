from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import func
from flask_jwt_extended import create_access_token, create_refresh_token

from fnote.extensions import db
from fnote.extensions import hashing
from fnote.config.settings import HASH_SALT_PW
from fnote.blueprints.user.exceptions import UserExistsError


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, server_default='')
    notes = relationship('Note')
    verified_email = db.Column(db.Boolean, nullable=False)

    # activity tracking
    time_of_reg = db.Column(db.DateTime(), nullable=False)
    login_count = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime(), nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.password = User.encrypt_pw(kwargs.get('password', ''))

    @classmethod
    def register(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        if User.find_by_identity(email):
            raise UserExistsError(email)

        new_user = User(email=email, password=password)
        now = datetime.utcnow()
        new_user.time_of_reg = now
        new_user.last_login = now
        new_user.login_count = 1
        new_user.verified_email = False

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @classmethod
    def find_by_identity(cls, email):
        """ Get user from email
        :param email:
        :type email: str
        :return: User
        """
        return User.query.filter(func.lower(User.email) ==
                                 func.lower(email)).first()

    @classmethod
    def encrypt_pw(cls, pw_plain):
        """ Encrypt with hashing method specified in fnote.config.settings
        :param pw_plain: Plaintext password
        :type pw_plain: str
        :return: str
        """
        return hashing.hash_value(pw_plain, salt=HASH_SALT_PW)

    def get_refresh_token(self):
        """ Get refresh JWT, which can be used to get an unfresh access
        token
        :return: JWT refresh token
        """
        tkn = create_refresh_token(identity=self.email)
        self.login_count += 1
        self.last_login = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return tkn

    def get_access_token(self, fresh=False):
        """ Get JSON web token to be stored by client, either fresh or unfresh
        (defaults to unfresh)
        :return: JWT access token
        """
        tkn = create_access_token(identity=self.email, fresh=fresh)
        return tkn

    def check_password(self, pw_plain):
        """Check plaintext password against database
        :param pw_plain: Plaintext password
        :type pw_plain: str
        :return: bool
        """
        return hashing.check_value(self.password, pw_plain, salt=HASH_SALT_PW)

    def verify_email(self):
        """Mark user's email as confirmed and allow them to log in
        :return: None
        """
        self.verified_email = True
        db.session.add(self)
        db.session.commit()
        return None

    def update_email(self, new_email):
        """Update user's email in database. Throws UserExistsError if new email
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
        """Update user's password in database.
        :param new_password: New password
        :type new_password: str
        :return: updated User object
        """
        self.password = User.encrypt_pw(new_password)
        db.session.add(self)
        db.session.commit()
        return self

    def get_notes(self):
        """Get all notes belonging to user
        :returns: List of Note objects
        """
        return self.notes
