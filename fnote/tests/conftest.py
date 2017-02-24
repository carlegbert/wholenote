import pytest

from fnote.app import create_app


@pytest.yield_fixture(scope='session')
def app():
    """
    :return: Flask application
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
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
