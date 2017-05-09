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
        assert response_data['msg'] == 'Note created'

    def test_post_from_refresh(self, client, refresh_token, session):
        auth = {'Authorization': 'Bearer ' + refresh_token}
        refresh = client.post('/api/v1.0/refresh', headers=auth)
        unfresh_tkn = get_json(refresh)['access_token']
        auth = {'Authorization': 'Bearer ' + unfresh_tkn}
        data = {'title': 'new_note', 'text': 'new_text'}
        response = post_json(client, URL, data, auth)
        response_data = get_json(response)
        assert response.status_code == 201
        assert response_data['msg'] == 'Note created'

    def test_post_new_bad_data(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        data = {'bad_param': 'new_note', 'also_bad': 'new_text'}
        response = post_json(client, URL, data, auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert response_data['msg'] == 'Missing parameters in JSON data'

    def test_post_new_no_data(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        response = client.post(URL, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert response_data['msg'] == 'Missing JSON data'

    def test_post_note_bad_jwt(self, client):
        auth = {'Authorization': 'Bearer: not_a_real_token'}
        data = {'title': 'new_note', 'text': 'new_text'}
        response = post_json(client, URL, data, auth)
        assert response.status_code == 422

    def test_post_long_title_shortens(self, client, unfresh_token):
        # title longer than 255 chars should shorten to 255
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        long_title = 'abcdefghijklmnopqrstuvwxyz' * 10
        expected_title = long_title[:255]
        data = {'title': long_title, 'text': 'new_text'}
        response = post_json(client, URL, data, auth)
        response_data = get_json(response)
        assert response.status_code == 201
        assert response_data['msg'] == 'Note created'
        assert response_data['note']['title'] == expected_title

    def test_duplicate_title_insert_fails(self, client, unfresh_token):
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        data = {'title': 'dupetitle', 'text': 'text'}
        response_one = post_json(client, URL, data, auth)
        response_two = post_json(client, URL, data, auth)
        response_data = get_json(response_two)
        assert response_one.status_code == 201
        assert response_two.status_code == 400
        assert 'title' in response_data['msg']
