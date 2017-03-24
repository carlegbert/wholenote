from sqlalchemy_utils import database_exists, create_database

from fnote.config.settings import SQLALCHEMY_DATABASE_URI
from fnote.extensions import db


def init_db():
    """ Initialize dev & test databases. Until project is closer to MVP,
    dev db resets every time. This will eventually be called by a deployment
    CLI rather than app.py.
    """
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)
    db.drop_all()
    db.create_all()

    test_db_uri = '{0}_test'.format(SQLALCHEMY_DATABASE_URI)
    if not database_exists(test_db_uri):
        create_database(test_db_uri)
