from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
