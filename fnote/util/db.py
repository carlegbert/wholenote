from sqlalchemy_utils import database_exists, create_database

from fnote.config.settings import SQLALCHEMY_DATABASE_URI
from fnote.extensions import db


def init_db():
    """
    initialize prod & test databases
    """
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)
        db.create_all()

    test_db_uri = '{0}_test'.format(SQLALCHEMY_DATABASE_URI)
    if not database_exists(test_db_uri):
        create_database(test_db_uri)
