from fnote.tests.json_helpers import post_json, get_json


URL = '/api/v1.0/login'


class TestLoginViews(object):
    def test_login_success(self, client, db, user):
        post_data = {'email': user.email, 'password': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Login for {0} successful'.format(user.email)
        assert response_data['access_token']
        assert response_data['message'] == msg
        assert response.status_code == 200

    def test_login_bad_pw(self, client, db, user):
        post_data = {'email': user.email, 'password': 'hunter1'}
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
        msg = 'Bad authentication data'
        assert response_data['error'] == msg
        assert response.status_code == 422

    def test_login_no_data(self, client, db):
        response = client.post(URL)
        assert response.status_code == 401
