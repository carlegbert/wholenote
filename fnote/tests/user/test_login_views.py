from fnote.blueprints.user.models import User
from fnote.tests.json_helpers import post_json, get_json


URL = '/api/v1.0/login'


class TestLoginViews(object):
    def test_login_success(self, client, db):
        User.register(email='logintest@localhost', password='hunter2')
        post_data = {'email': 'logintest@localhost', 'password': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Login for logintest@localhost successful'
        assert response_data['access_token']
        assert response_data['message'] == msg
        assert response.status_code == 200

    def test_login_bad_pw(self, client, db):
        post_data = {'email': 'logintest@localhost', 'password': 'hunter1'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Login failed (incorrect email or password)'
        assert response_data['error'] == msg
        assert response.status_code == 403

    def test_login_bad_email(self, client, db):
        post_data = {'email': 'godzilla@tokyo', 'password': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Login failed (incorrect email or password)'
        assert response_data['error'] == msg
        assert response.status_code == 403

    def test_login_bad_data(self, client, db):
        post_data = {'badparam': 'stuff', 'passwrod': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Bad request'
        assert response_data['error'] == msg
        assert response.status_code == 400

    def test_login_no_data(self, client, db):
        response = client.post(URL)
        response_data = get_json(response)
        msg = 'Bad request'
        assert response_data['error'] == msg
        assert response.status_code == 400
