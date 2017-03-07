import pytest

from fnote.app import create_app
from fnote.blueprints.user.models import User
from fnote.config.settings import SQLALCHEMY_DATABASE_URI
from fnote.extensions import db as _db


@pytest.yield_fixture(scope='session')
def app():
    """
    :return: Flask application
    """
    test_db_uri = '{0}_test'.format(SQLALCHEMY_DATABASE_URI)
    params = {
        'DEBUG': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_db_uri
    }

    _app = create_app(settings_override=params)

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Set up test db
    :param app: Pytest fixture
    :return: SQLAlchemy DB session
    """
    _db.drop_all()
    _db.create_all()

    # create single user for use in tests
    test_user = User(email='testuser@localhost', password='hunter2')
    _db.session.add(test_user)
    _db.session.commit()

    return _db


@pytest.fixture(scope='session')
def session(db):
    db.session.begin_nested()
    yield db.session
    db.session.rollback
