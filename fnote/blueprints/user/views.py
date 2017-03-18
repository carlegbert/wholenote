from flask import (
        abort,
        Blueprint,
        jsonify,
        make_response,
        request,
        )
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from fnote.blueprints.user.exceptions import UserExistsError
from fnote.blueprints.user.models import User


user = Blueprint('user', __name__)


@user.route('/api/v1.0/login', methods=['POST'])
def login():
    """ Accepts JSON login request.
    :returns: JSON with status code, message, fresh access token,
    and refresh token.
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
        access_token = u.get_access_token(True)
        refresh_token = u.get_refresh_token()
        msg = 'Login for {0} successful'.format(email)
        data = {'message': msg, 'access_token': access_token,
                'refresh_token': refresh_token, 'statusCode': 200}
        return make_response(jsonify(data), 200)
    except KeyError:
        abort(422)


@user.route('/api/v1.0/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Accepts request with refresh token in header and returns JSON response
    with nonfresh access token, which can then be used to request resources.
    The server will not redirect requests containing timed-out access tokens;
    it is the responsibility of the client to request a new access token when
    the old one has timed out.
    :returns: JSON with status code, message, nonfresh access token
    """
    email = get_jwt_identity()
    u = User.find_by_identity(email)
    jwt = u.get_access_token()
    data = {'access_token': jwt, 'message': 'Success', 'statusCode': 200}
    return make_response(jsonify(data), 200)


@user.route('/api/v1.0/register', methods=['POST'])
def register():
    """Accepts JSON registration request and inserts user into database.
    :returns: JSON with status code, message, refresh token, fresh access token
    """
    try:
        email = request.json['email']
        password = request.json['password']
        u = User.register(email=email, password=password)
        access_token = u.get_access_token(True)
        refresh_token = u.get_refresh_token()
        message = 'Account registered for {0}.'.format(u.email)
        status_code = 200
        res = {'statusCode': 200, 'message': message,
               'access_token': access_token, 'refresh_token': refresh_token}
    except UserExistsError:
        status_code = 400
        res = {'statusCode': 400,
               'error': 'Account already registered for that email'}
    except (AttributeError, TypeError, KeyError):
        abort(400)
    return make_response(jsonify(res), status_code)
