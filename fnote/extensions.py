from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from flask_jwt_extended import JWTManager
from hashids import Hashids
from fnote.config.settings import HASHID_SALT

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
hashing = Hashing()
jwt = JWTManager()
hashids = Hashids(HASHID_SALT, min_length=8)
