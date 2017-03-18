from fnote.tests.json_helpers import get_json


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

    def test_refresh_fresh_in_header(self, client, fresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(fresh_token)}
        response = client.post(URL, headers=auth)
        assert response.status_code == 422

    def test_refresh_unfresh_in_header(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(unfresh_token)}
        response = client.post(URL, headers=auth)
        assert response.status_code == 422
