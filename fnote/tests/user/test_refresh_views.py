from fnote.tests.json_helpers import get_json
from fnote.blueprints.user.models import User


URL = '/api/v1.0/refresh'


class TestRefreshViews(object):
    def test_refresh_success(self, client, db, refresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(refresh_token)}
        response = client.post(URL, headers=auth)
        response_data = get_json(response)
        assert response_data['access_token']
        assert response.status_code == 200

    def test_refresh_wrong_method(self, client, db, refresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(refresh_token)}
        response = client.get(URL, headers=auth)
        assert response.status_code == 405

    def test_refresh_no_header(self, client):
        response = client.post(URL)
        assert response.status_code == 401

    def test_refresh_bad_header(self, client):
        bad_jwt_str = 'thisisnotavalidJWTstring'
        auth = {'Authorization': 'Bearer {0}'.format(bad_jwt_str)}
        response = client.post(URL, headers=auth)
        assert response.status_code == 422

    def test_refresh_wrong_auth(self, client, auth_header):
        # sending username/password authentication header instead of token
        response = client.post(URL, headers=auth_header)
        assert response.status_code == 422

    def test_refresh_fresh_in_header(self, client, fresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(fresh_token)}
        response = client.post(URL, headers=auth)
        assert response.status_code == 422

    def test_refresh_unfresh_in_header(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(unfresh_token)}
        response = client.post(URL, headers=auth)
        assert response.status_code == 422

    def test_get_refresh_and_use(self, client, auth_header):
        response_one = client.post('/api/v1.0/login', headers=auth_header)
        refresh_token = get_json(response_one)['refresh_token']
        refresh_header = {'Authorization': 'Bearer {0}'.format(refresh_token)}
        response_two = client.post(URL, headers=refresh_header)
        assert response_one.status_code == 200
        assert response_two.status_code == 200

    def test_get_access_unverified(self, client, session):
        unver_user = User.register(email='unver@email',
                                   password='hunter2password')
        rtkn = unver_user.get_refresh_token()
        headers = {'Authorization': 'Bearer {0}'.format(rtkn)}
        response = client.post(URL, headers=headers)
        response_data = get_json(response)
        assert response.status_code == 403
        assert response_data['msg'] == 'Unverified email address'
