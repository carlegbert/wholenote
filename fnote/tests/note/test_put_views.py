from fnote.tests.json_helpers import get_json, put_json
from fnote.blueprints.note.models import Note
from fnote.extensions import hashids


URL = '/api/v1.0/notes'


class TestPutNoteViews(object):

    #  Tests with bad authorization, wrong note id, etc are redundant with GET
    #  tests since they use the same view, so they are mostly not repeated here

    def test_put_single_note(self, client, user, unfresh_token, session):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, hashids.encode(note.id))
        data = {'title': 'new_title', 'text': 'new_text'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['note']
        assert response_data['note']['title'] == 'new_title'
        assert response_data['note']['text'] == 'new_text'

    def test_put_doesnt_insert(self, client, user, unfresh_token, session):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, hashids.encode(note.id))
        data = {'title': 'new_title', 'text': 'new_text'}
        before_len = len(Note.query.all())
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        after_len = len(Note.query.all())
        assert response.status_code == 200
        assert response_data['note']['title'] == 'new_title'
        assert after_len == before_len

    def test_put_note_with_refresh(self, client, user, refresh_token, session):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+refresh_token}
        refresh = client.post('/api/v1.0/refresh', headers=auth)
        unfresh_tkn = get_json(refresh)['access_token']
        auth = {'AUthorization': 'Bearer ' + unfresh_tkn}
        url = '{0}/{1}'.format(URL, hashids.encode(note.id))
        data = {'title': 'new_title', 'text': 'new_text'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['note']
        assert response_data['note']['title'] == 'new_title'
        assert response_data['note']['text'] == 'new_text'

    def test_put_note_bad_data(self, client, user, unfresh_token):
        # Update request with no valid params in JSON should return a 400
        # and list note properties that can be updated.
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, hashids.encode(note.id))
        data = {'x': 'y', 'z': 'a'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert 'Missing parameters in JSON data' in response_data['error']

    def test_put_note_no_data(self, client, user, unfresh_token):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, hashids.encode(note.id))
        response = client.put(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert 'Missing JSON data' in response_data['error']
