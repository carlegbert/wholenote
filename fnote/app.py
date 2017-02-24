from flask import Flask

from fnote.blueprints.index import index
from fnote.blueprints.user import user


def create_app(settings_override=None):
    """
    :return: flask app
    """
    app = Flask(__name__)

    app.register_blueprint(index)
    app.register_blueprint(user)

    if settings_override:
        app.config.update(settings_override)

    return app
