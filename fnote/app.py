from flask import Flask

from fnote.blueprints.page import page
from fnote.blueprints.user import user
from fnote.blueprints.note import note
from fnote.util.db import init_db
from fnote.errorhandlers import register_errorhandlers
from fnote.extensions import (
    debug_toolbar,
    db,
    hashing,
    jwt,
)


def create_app(settings_override=None):
    """
    :return: flask app
    """
    app = Flask(__name__)

    app.config.from_object('fnote.config.settings')

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(note)
    extensions(app)
    register_errorhandlers(app)

    db.app = app
    init_db()  # TODO: better db creation script

    return app


def extensions(app):
    """
    Add extensions to flask application
    :param app: Flask application
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)
    hashing.init_app(app)
    jwt.init_app(app)

    return None
