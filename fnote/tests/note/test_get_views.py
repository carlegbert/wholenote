from fnote.blueprints.user.models import User
from fnote.tests.json_helpers import get_json


URL = '/api/v1.0/notes'


class TestGetNoteViews(object):
    def test_get_notes_for_user(self, client, db, user, note, unfresh_token):
        auth = {'Authorization': 'Bearer {0}'.format(unfresh_token)}
        response = client.get(URL, headers=auth)
        response_data = get_json(response)
        assert response_data['notes']
        assert response_data['notes'][str(note.id)]
        assert response_data['notes'][str(note.id)]['text'] == note.text
        assert response.status_code == 200

    def test_get_notes_bad_jwt(self, client, db):
        bad_jwt_str = 'thisisnotavalidJWTstring'
        auth = {'Authorization': 'Bearer {0}'.format(bad_jwt_str)}
        response = client.get(URL, headers=auth)
        assert response.status_code == 422

    def test_get_notes_no_jwt(self, client, db):
        response = client.get(URL)
        assert response.status_code == 401

    def test_get_single_note(self, client, db, user, note):
        jwt = user.get_access_token()
        auth = {'Authorization': 'Bearer {0}'.format(jwt)}
        url = '{0}/{1}'.format(URL, note.id)
        response = client.get(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 200
        assert response_data
        assert response_data['id'] == note.id

    def test_single_note_bad_jwt(self, client, db, note):
        bad_jwt_str = 'thisisnotavalidJWTstring'
        auth = {'Authorization': 'Bearer {0}'.format(bad_jwt_str)}
        url = '{0}/{1}'.format(URL, note.id)
        response = client.get(url, headers=auth)
        assert response.status_code == 422

    def test_single_note_wrong_jwt(self, client, db, user, note, session):
        u_2 = User.register(email='wronguser@localhost', password='hunter2')
        jwt = u_2.get_access_token()
        auth = {'Authorization': 'Bearer {0}'.format(jwt)}
        url = '{0}/{1}'.format(URL, note.id)
        response = client.get(url, headers=auth)
        response_data = get_json(response)
        assert response.status_code == 403
        assert u_2.email in response_data['error']

    def test_single_note_no_jwt(self, client, db, note):
        url = '{0}/{1}'.format(URL, note.id)
        response = client.get(url)
        assert response.status_code == 401

    def test_single_note_bad_id(self, client, db, user, note, unfresh_token):
        nid = note.id + 1
        auth = {'Authorization': 'Bearer {0}'.format(unfresh_token)}
        url = '{0}/{1}'.format(URL, nid)
        response = client.get(url, headers=auth)
        assert response.status_code == 404
