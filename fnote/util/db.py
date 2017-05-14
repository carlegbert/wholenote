from fnote.extensions import db


def init_db():
    """ Create database tables """
    db.create_all()
