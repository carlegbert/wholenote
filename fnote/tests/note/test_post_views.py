from fnote.tests.json_helpers import get_json, post_json


URL = '/api/v1.0/notes'


class TestPostNoteViews(object):
    # Tests with bad authorization, wrong note id, etc are redundant with GET
    # tests since they use the same view, so they are mostly not repeated here.
    def test_post_new_note(self, client, unfresh_token, session):
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        data = {'title': 'new_note', 'text': 'new_text'}
        response = post_json(client, URL, data, auth)
        response_data = get_json(response)
        assert response.status_code == 201
        assert response_data['message'] == 'Note created'

    def test_post_from_refresh(self, client, refresh_token, session):
        auth = {'Authorization': 'Bearer ' + refresh_token}
        refresh = client.post('/api/v1.0/refresh', headers=auth)
        unfresh_tkn = get_json(refresh)['access_token']
        auth = {'Authorization': 'Bearer ' + unfresh_tkn}
        data = {'title': 'new_note', 'text': 'new_text'}
        response = post_json(client, URL, data, auth)
        response_data = get_json(response)
        assert response.status_code == 201
        assert response_data['message'] == 'Note created'

    def test_post_new_bad_data(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        data = {'bad_param': 'new_note', 'also_bad': 'new_text'}
        response = post_json(client, URL, data, auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert response_data['error'] == 'Missing parameters in JSON data'

    def test_post_new_no_data(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        response = client.post(URL, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert response_data['error'] == 'Missing JSON data'

    def test_post_note_bad_jwt(self, client):
        auth = {'Authorization': 'Bearer: not_a_real_token'}
        data = {'title': 'new_note', 'text': 'new_text'}
        response = post_json(client, URL, data, auth)
        assert response.status_code == 422