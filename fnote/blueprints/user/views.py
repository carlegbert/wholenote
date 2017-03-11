from flask import (
        abort,
        Blueprint,
        jsonify,
        make_response,
        request,
        )

from fnote.blueprints.user.exceptions import UserExistsError
from fnote.blueprints.user.models import User


user = Blueprint('user', __name__)


@user.route('/api/v1.0/login', methods=['POST'])
def login():
    """TODO: Docstring for login
    :returns: TODO

    """
    # Ensure correct data is present
    # Check for existing user
    # Check for correct pw
    # Return JSON with some sort of token + 200
    # Return JSON with failure message + 400
    pass


@user.route('/api/v1.0/register', methods=['POST'])
def register():
    """Accepts JSON registration request and inserts user into database.
    :returns: JSON with status code and message
    """
    try:
        email = request.json['email']
        password = request.json['password']
        u = User.register(email=email, password=password)
        message = 'Account registered for {0}.'.format(u.email)
        status_code = 200
        res = {'statusCode': 200, 'message': message}
    except UserExistsError:
        status_code = 400
        res = {'statusCode': 400,
               'message': 'Account already registered for that email'}
    except (AttributeError, TypeError, KeyError):
        status_code = 400
        res = {'statusCode': 400, 'message': 'Data missing from request'}

    return make_response(jsonify(res), status_code)
