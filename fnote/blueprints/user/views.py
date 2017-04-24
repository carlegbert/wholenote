from flask import (
        abort,
        Blueprint,
        jsonify,
        make_response,
        redirect,
        render_template,
        request,
        url_for,
        )

from validate_email import validate_email
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity

from .exceptions import UserExistsError
from .models import User
from .mail import send_confirmation_message
from fnote.extensions import url_sts


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/api/v1.0/login', methods=['POST'])
def login():
    """ Accepts login request with HTTP Basic auth header
    :returns: JSON with status code, message, fresh access token,
    and refresh token.
    """
    auth = request.authorization
    if not auth:
        abort(422)

    email = auth.username
    password = auth.password
    u = User.find_by_identity(email)

    if not u or not u.check_password(password):
        data = {'error': 'Login failed (incorrect email or password)',
                'statusCode': 403}
        return make_response(jsonify(data), 403)
    elif not u.verified_email:
        # Front-end client should provide link to resend verification email
        data = {'error': 'Unverified email address', 'statusCode': 403}
        return make_response(jsonify(data), 403)

    access_token = u.get_access_token(True)
    refresh_token = u.get_refresh_token()
    msg = 'Login for {0} successful'.format(email)
    data = {'message': msg, 'access_token': access_token,
            'refresh_token': refresh_token, 'statusCode': 200}
    return make_response(jsonify(data), 200)


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
    if not u.verified_email:
        data = {'error': 'Unverified email address', 'statusCode': 403}
        return make_response(jsonify(data), 403)
    jwt = u.get_access_token()
    data = {'access_token': jwt, 'message': 'Success',
            'email': email, 'statusCode': 200}
    return make_response(jsonify(data), 200)


@user.route('/api/v1.0/register', methods=['POST'])
def register():
    """Accepts JSON registration request and inserts user into database.
    :returns: JSON with status code, message, refresh token
    """
    try:
        email = request.json['email']
        password = request.json['password']

        if not validate_email(email):
            data = {'error': email+' is not a valid email address',
                    'statusCode': 400}
            return make_response(jsonify(data), 400)

        if len(password) < 10:
            data = {'error': 'Password must be at least 10 characters',
                    'statusCode': 400}
            return make_response(jsonify(data), 400)

        u = User.register(email=email, password=password)
        refresh_token = u.get_refresh_token()

        message = 'Account registered for {0}.'.format(u.email)
        send_confirmation_message(u.email)
        # frontend client should remind user to verify their email
        res = {'statusCode': 200, 'message': message, 'refresh_token': refresh_token}
        return make_response(jsonify(res), 200)

    except UserExistsError:
        res = {'statusCode': 400,
               'error': 'Account already registered for that email'}
        return make_response(jsonify(res), 400)

    except (AttributeError, TypeError, KeyError):
        abort(400)


@user.route('/verify/<tkn>', methods=['GET'])
def verify(tkn):
    """URL for email-verification (email should be sent when request is sent
    to register route). Token in email does not expire.
    :returns: HTML page
    """
    try:
        unloaded = url_sts.loads(tkn)

        if unloaded[0] == 'verify_email':
            u = User.find_by_identity(unloaded[1])
            u.verify_email()
            # this should actually return page saying registration succeeded
            # (make seperate template, don't redirect)
            return render_template('user/verify_success.html')
        else:
            return render_template('user/verify_fail.html')
    except Exception:
        return render_template('user/verify_fail.html')
