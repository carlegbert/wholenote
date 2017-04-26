from ..json_helpers import post_json, get_json


URL = '/api/v1.0/register'


class TestRegisterViews(object):
    def test_register_new_user_success(self, client, db, session):
        post_data = {'email': 'newuser@localhost',
                     'password': 'hunter2password'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Account registered for {0}'.format('newuser@localhost.')
        assert msg in response_data['message']
        assert response_data['refresh_token']
        assert response.status_code == 200

    def test_register_user_exists(self, client, db):
        post_data = {'email': 'testuser@localhost',
                     'password': 'hunter2password'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Account already registered for that email'
        assert response_data['error'] == msg
        assert response.status_code == 400

    def test_register_no_data(self, client):
        response = client.post(URL)
        response_data = get_json(response)
        msg = 'Bad request'
        assert response_data['error'] == msg
        assert response.status_code == 400

    def test_register_bad_data(self, client):
        post_data = {'bad_param': 'testuser@localhost',
                     'passwrod': 'hunter2password'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Bad request'
        assert response_data['error'] == msg
        assert response.status_code == 400

    def test_register_bad_email(self, client):
        post_data = {'email': 'not_real_address',
                     'password': 'hunter2password'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        assert 'not_real_address' in response_data['error']
        assert response.status_code == 400

    def test_register_short_password_fails(self, client):
        post_data = {'email': 'testuser2@localhost',
                     'password': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        assert 'Password must be at least' in response_data['error']
        assert response.status_code == 400

    def test_long_email_sends_error(self, client):
        long_email = 'a' * 246 + '@gmail.com'
        post_data = {'email': long_email, 'password': 'hunter2password'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        assert 'Max email length is 255 characters' in response_data['error']
        assert response.status_code == 400

    def test_long_password_sends_error(self, client):
        long_password = 'a' * 129
        post_data = {'email': 'testuser3@localhost', 'password': long_password}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        assert 'Max password length is 128 characters' in response_data['error']
        assert response.status_code == 400
