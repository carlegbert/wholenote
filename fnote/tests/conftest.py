from base64 import b64encode
import pytest

from fnote.app import create_app
from fnote.blueprints.user.models import User
from fnote.blueprints.note.models import Note
from fnote.config.settings import SQLALCHEMY_DATABASE_URI
from fnote.extensions import db as _db
from fnote.extensions import hashids
from fnote.extensions import mail as _mail


@pytest.fixture(scope='session')
def app():
    """
    :return: Flask application
    """
    test_db_uri = '{0}_test'.format(SQLALCHEMY_DATABASE_URI)
    params = {
        'DEBUG': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_db_uri,
    }

    _app = create_app(settings_override=params)

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """ Set up app client. Executed for every test.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='function')
def session(db, request):
    """ Roll back db in between tests using nested session.
    This fixture should be used for any test that updates the
    database.
    :param db: Pytest fixture
    :return: None
    """
    db.session.begin_nested()

    def teardown():
        db.session.rollback()

    request.addfinalizer(teardown)

    return db.session


@pytest.fixture(scope='session')
def db(app):
    """ Set up test db. Executed once every time that tests are run.
    :param app: Pytest fixture
    :return: SQLAlchemy DB session
    """
    _db.drop_all()
    _db.create_all()

    # Create single user and single note, accessible by using the 'user' and
    # 'note' fixtures below.  If these are mutated, be sure to use the
    # 'session' fixture so that they are rolled back to normal for other tests.
    u = User.register(email='testuser@localhost', password='hunter2password')
    u.verify_email()

    n = Note(u.id, 'test_note', 'text')
    _db.session.add(n)
    _db.session.commit()

    return _db


@pytest.fixture(scope='session')
def user(db):
    """Return test user inserted in db fixture. For use in tests that use
    but will not mutate a user.
    :param db: Pytest fixture
    :return: User object
    """
    return User.find_by_identity('testuser@localhost')


@pytest.fixture(scope='session')
def note(db):
    """Return test note inserted in db fixture. For use in tests that use but
    will not mutate a note.
    :param db: Pytest fixture
    :return: Note object
    """
    return Note.query.filter(Note.title == 'test_note').first()


@pytest.fixture(scope='session')
def refresh_token(user):
    """Return refresh token from user fixture
    :param user: Pytest fixture
    :return: JWT Refresh Token
    """
    return user.get_refresh_token()


@pytest.fixture(scope='session')
def unfresh_token(user):
    """Return unfresh token from user fixture
    :param user: Pytest fixture
    :return: Unfresh JWT access token
    """
    return user.get_access_token()


@pytest.fixture(scope='session')
def fresh_token(user):
    """Return fresh token from user fixture
    :param user: Pytest fixture
    :return: Fresh jwt access token
    """
    return user.get_access_token(True)


@pytest.fixture(scope='session')
def auth_header():
    """Return dict object containing b64 encoded
    Basic Authorization header
    :return: Authorization header
    """
    encstr = b64encode(b'testuser@localhost:hunter2password').decode('utf-8')
    auth = {'Authorization': 'Basic {0}'.format(encstr)}
    return auth


@pytest.fixture(scope='session')
def hash_id(note):
    """Return hashed id from seed note
    :param note: Pytest fixture
    :return: hash string from note.id
    """
    return hashids.encode(note.id)


@pytest.fixture(scope='session')
def mail(app):
    """Return configured mail object for use in tests
    :param app: Pytest fixture
    :return: Mail object
    """
    return _mail
