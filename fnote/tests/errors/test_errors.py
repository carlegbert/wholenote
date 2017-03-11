from flask import url_for
from fnote.tests.json_helpers import get_json


class TestErrorHandlers(object):
    def test_bad_method(self, client):
        response = client.get(url_for('user.register'))
        response_data = get_json(response)
        assert response.status_code == 405
        assert response_data['error'] == 'Method not allowed'

    def test_not_found(self, client):
        response = client.get('/not/a/real/url')
        response_data = get_json(response)
        assert response.status_code == 404
        assert response_data['error'] == 'Not found'
