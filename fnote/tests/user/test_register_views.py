from fnote.blueprints.user.models import User
from fnote.tests.json_helpers import post_json, get_json


URL = '/api/v1.0/register'


class TestRegisterViews(object):
    def test_register_new_user_success(self, client, db):
        post_data = {'email': 'newuser@localhost', 'password': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Account registered for {0}'.format('newuser@localhost.')
        assert response_data['message'] == msg
        assert response_data['statusCode'] == 200

    def test_register_user_exists(self, client, db):
        User.register(email='existinguser@localhost', password='hunter2')
        post_data = {'email': 'existinguser@localhost', 'password': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Account already registered for that email'
        assert response_data['message'] == msg
        assert response_data['statusCode'] == 400

    def test_register_no_json(self, client):
        response = client.post(URL)
        response_data = get_json(response)
        msg = 'Data missing from request'
        assert response_data['message'] == msg
        assert response_data['statusCode'] == 400

    def test_register_bad_data(self, client):
        post_data = {'bad_param': 'testuser@localhost', 'passwrod': 'hunter2'}
        response = post_json(client, URL, post_data)
        response_data = get_json(response)
        msg = 'Data missing from request'
        assert response_data['message'] == msg
        assert response_data['statusCode'] == 400
