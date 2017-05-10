from fnote.tests.json_helpers import get_json, put_json
from fnote.blueprints.note.models import Note


URL = '/api/v1.0/notes'


class TestPutNoteViews(object):

    #  Tests with bad authorization, wrong note id, etc are redundant with GET
    #  tests since they use the same view, so they are mostly not repeated here

    def test_put_single_note(self, client, user, unfresh_token, session):
        note = Note(user.id, 'put_note', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, note.title)
        data = {'title': 'new_title1', 'text': 'new_text'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['note']
        assert response_data['note']['title'] == 'new_title1'
        assert response_data['note']['text'] == 'new_text'

    def test_put_update_date(self, client, user, unfresh_token, session):
        note = Note(user.id, 'put_note', 'text').save()
        old_date = note.last_modified
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, note.title)
        data = {'title': 'new_title2', 'text': 'new_text'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        new_date = response_data['note']['lastModified']
        assert new_date != old_date

    def test_put_doesnt_insert(self, client, user, unfresh_token, session):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, note.title)
        data = {'title': 'new_title3', 'text': 'new_text'}
        before_len = len(Note.query.all())
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        after_len = len(Note.query.all())
        assert response.status_code == 200
        assert response_data['note']['title'] == 'new_title3'
        assert after_len == before_len

    def test_put_note_with_refresh(self, client, user, refresh_token, session):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+refresh_token}
        refresh = client.post('/api/v1.0/refresh', headers=auth)
        unfresh_tkn = get_json(refresh)['access_token']
        auth = {'AUthorization': 'Bearer ' + unfresh_tkn}
        url = '{0}/{1}'.format(URL, note.title)
        data = {'title': 'new_title4', 'text': 'new_text'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['note']
        assert response_data['note']['title'] == 'new_title4'
        assert response_data['note']['text'] == 'new_text'

    def test_put_note_bad_data(self, client, user, unfresh_token, session):
        # Update request with no valid params in JSON should return a 400
        # and list note properties that can be updated.
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, note.title)
        data = {'x': 'y', 'z': 'a'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert 'Missing parameters in JSON data' in response_data['msg']

    def test_put_note_no_data(self, client, user, unfresh_token, session):
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer '+unfresh_token}
        url = '{0}/{1}'.format(URL, note.title)
        response = client.put(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 400
        assert 'Missing JSON data' in response_data['msg']

    def test_put_long_title(self, client, user, unfresh_token, session):
        # title longer than 255 chars should shorten to 255
        note = Note(user.id, 'title', 'text').save()
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        long_title = 'abcdefghijklmnopqrstuvwxyy' * 10
        expected_title = long_title[:255]
        url = '{0}/{1}'.format(URL, note.title)
        data = {'title': long_title, 'text': 'new_text'}
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data['note']['title'] == expected_title

    def test_same_title_update(self, client, unfresh_token, user, session):
        note1 = Note(user.id, 'duplicatetitle', 'text').save()
        note2 = Note(user.id, 'uniquetitle', 'text').save()
        auth = {'Authorization': 'Bearer ' + unfresh_token}
        data = {'title': note1.title}
        url = '{0}/{1}'.format(URL, note2.title_id)
        response = put_json(client, url, data, auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert note2.title_id == 'duplicatetitle2'
        assert response_data['note']['id'] == 'duplicatetitle2'
