from base64 import b64encode
from fnote.tests.json_helpers import get_json


URL = '/api/v1.0/login'


class TestLoginViews(object):
    def test_login_success(self, client, db, auth_header):
        response = client.post(URL, headers=auth_header)
        response_data = get_json(response)
        msg = 'Login for {0} successful'.format('testuser@localhost')
        assert response_data['refresh_token']
        assert response_data['access_token']
        assert response_data['message'] == msg
        assert response.status_code == 200

    def test_login_updates_activity_tracking(self, client, user, auth_header):
        old_login_count = user.login_count
        old_login_date = user.last_login
        client.post(URL, headers=auth_header)
        new_login_count = user.login_count
        new_login_date = user.last_login
        assert new_login_count == old_login_count + 1
        assert new_login_date != old_login_date

    def test_login_bad_pw(self, client, db):
        encstr = b64encode(b'testuser@localhost:wrong').decode('utf-8')
        auth = {'Authorization': 'Basic {0}'.format(encstr)}
        response = client.post(URL, headers=auth)
        response_data = get_json(response)
        msg = 'Login failed (incorrect email or password)'
        assert response_data['error'] == msg
        assert response.status_code == 403

    def test_login_bad_email(self, client, db):
        encstr = b64encode(b'not@realuser:hunter2').decode('utf-8')
        auth = {'Authorization': 'Basic {0}'.format(encstr)}
        response = client.post(URL, headers=auth)
        response_data = get_json(response)
        msg = 'Login failed (incorrect email or password)'
        assert response_data['error'] == msg
        assert response.status_code == 403

    def test_login_bad_header(self, client, db):
        encstr = b64encode(b'not@realuser:hunter2').decode('utf-8')
        auth = {'Authorization': 'WrongWord {0}'.format(encstr)}
        response = client.post(URL, headers=auth)
        assert response.status_code == 422

    def test_login_wrong_method(self, client, db, user, auth_header):
        response = client.get(URL, headers=auth_header)
        assert response.status_code == 405

    def test_login_no_header(self, client, db):
        response = client.post(URL)
        assert response.status_code == 422
