from flask import (
        Blueprint,
        redirect,
        request,
        )

from fnote.blueprints.user.exceptions import UserExistsError
from fnote.blueprints.user.models import User


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/api/v1.0/login', methods=['POST'])
def login():
    # Ensure correct data is present
    # Check for existing user
    # Check for correct pw
    # Return JSON with some sort of token + 200
    # Return JSON with failure message + 500
    pass


@user.route('/api/v1.0/register', methods=['GET', 'POST'])
def register():
    # Ensure correct data is present
    # Check for existing user
    # Check for confirmed pw
    # insert user into DB
    # send confirmation email
    # Return JSON with some sort of token + 200
    # Return JSON with failure message + 500
    pass
