from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from flask_jwt_extended import JWTManager

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
hashing = Hashing()
jwt = JWTManager()
