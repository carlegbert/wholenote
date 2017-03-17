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
    """ Accepts JSON login request and returns JSON containing JWT token.
    :returns: JSON with status code, message, and JWT
    """
    try:
        if not request.json:
            abort(401)
        email = request.json['email']
        password = request.json['password']
        u = User.find_by_identity(email)
        if not u or not u.check_password(password):
            data = {'error': 'Login failed (incorrect email or password)',
                    'statusCode': 403}
            return make_response(jsonify(data), 403)
        jwt = u.get_jwt()
        msg = 'Login for {0} successful'.format(email)
        res = {'message': msg, 'access_token': jwt, 'statusCode': 200}
        return make_response(jsonify(res), 200)
    except KeyError:
        abort(422)


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
               'error': 'Account already registered for that email'}
    except (AttributeError, TypeError, KeyError):
        abort(400)
    return make_response(jsonify(res), status_code)
