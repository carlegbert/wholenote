from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from hashids import Hashids
from fnote.config.settings import HASHID_SALT, STS_SECRET_KEY
from itsdangerous import URLSafeTimedSerializer

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
hashing = Hashing()
hashids = Hashids(HASHID_SALT, min_length=8)
jwt = JWTManager()
mail = Mail()
url_sts = URLSafeTimedSerializer(STS_SECRET_KEY)
